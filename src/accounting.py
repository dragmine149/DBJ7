import random
import typing
from datetime import datetime, timedelta

import discord
from discord.ext import commands

from .utils import bank


class Accounting(commands.Cog):
    """
    Accouting group command
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        bank.bot = self.bot
        self.bot.loop.create_task(self.add_non_existing_users())

    async def add_non_existing_users(self):
        await self.bot.wait_until_ready()
        for member in self.bot.get_all_members():
            await bank.Player_Status.initialize_new_user(
                member.id
            ) if not member.bot and not member.id in await bank.Player_Status.get_users() else None

    @property
    def display_emoji(self) -> typing.Union[str, bytes, discord.PartialEmoji]:
        return "💰"

    @commands.hybrid_group()
    async def account(self, ctx: commands.Context) -> None:
        """
        Accounting group commands (where you can send money,get daily money,etc)
        """
        if not ctx.subcommand_passed:
            await ctx.send_help(ctx.command)

    @account.command()
    async def info(self, ctx: commands.Context, member: discord.User = None):
        member = member if member else ctx.author
        if member.bot:
            return await ctx.reply(
                embed=discord.Embed(title="No.", color=discord.Color.red())
            )
        account = await bank.Player_Status.get_by_id(
            member.id if member else ctx.author.id
        )

        authorBalenceEmbed = discord.Embed(
            title=f"{str(member) if member else str(ctx.author)}'s balance",
            color=discord.Color.green(),
        )
        authorBalenceEmbed.add_field(
            name="Balance",
            value=account.money,
        )
        authorBalenceEmbed.add_field(name="Debt", value=account.debt)
        authorBalenceEmbed.add_field(name="Unluckiness", value=account.unlucky)

        await ctx.reply(embed=authorBalenceEmbed)

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @account.command()
    async def daily(self, ctx: commands.Context):
        account = await bank.Player_Status.get_by_id(ctx.author.id)
        account.money += 1000
        await ctx.reply(
            embed=discord.Embed(
                title="Daily prize!",
                description="You got 1000 coins for daily prize!",
                color=discord.Color.green(),
            )
        )

    @daily.error
    async def daily_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(
                embed=discord.Embed(
                    title="Daily prize!",
                    description=f"You can get daily prize in {timedelta(seconds=error.cooldown.get_retry_after())}!",
                )
            )
        else:
            raise error

    @account.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def pay_debt(
        self, ctx: commands.Context, pay: int = random.randint(100, 500)
    ):
        account = await bank.Player_Status.get_by_id(ctx.author.id)
        if pay > account.money:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Pay debt",
                    description="You don't have enough money to pay debt! Try again next 5 minutes!",
                )
            )
        if pay > account.debt:
            account.money = pay - account.debt
            account.debt = 0
            account.last_paid_debt = None
        else:
            account.debt -= pay
            account.last_paid_debt = datetime.now()

        await ctx.reply(
            embed=discord.Embed(
                title="Your debt has been all paid off! Congratulations!"
                if not account.debt
                else f"You paid {pay} for your debt and now you can gamble again!",
                description="Enjoy your gambling and don't make debt next time!"
                if not account.debt
                else "Gamble carefully next time and paid these debts off! Also you can risk unable to gamble after 1 week of not paying your debt!",
                color=discord.Color.green(),
            )
        )

    @pay_debt.error
    async def pay_debt_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(
                embed=discord.Embed(
                    title="Pay debt",
                    description=f"You can pay debt in {timedelta(seconds=error.cooldown.get_retry_after())}!",
                )
            )
        else:
            raise error

    @account.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def borrow_money(self, ctx: commands.Context, amount: int = 1000):
        account = await bank.Player_Status.get_by_id(ctx.author.id)
        interest = round(random.random(),2)
        if (datetime.now() - (account.last_paid_debt if account.last_paid_debt else datetime.now())).days > 7:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Borrow money",
                    description="You can't borrow money because you didn't pay your debt for 1 week!",
                    color=discord.Color.red(),
                )
            )
        account.debt += amount + (amount * interest)
        account.last_paid_debt = datetime.now()
        account.money += amount

        await ctx.reply(
            embed=discord.Embed(
                title="Successfully borrowed money!",
                description=f"You've borrowed {amount} and interest is {interest} and that's mean you need to paid {amount + (amount * interest)} and beware that you will unable to gamble if you don't pay any debt in a week!",
                color=discord.Color.random(),
            )
        )

    @borrow_money.error
    async def borrow_money_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(
                embed=discord.Embed(
                    title="Borrow money",
                    description=f"You can borrow money 1 time per day! Please wait for another {timedelta(seconds=error.cooldown.get_retry_after())}",
                )
            )
        else:
            raise error


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Accounting(bot))
