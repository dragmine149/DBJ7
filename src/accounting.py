import typing

import discord
from discord.ext import commands, tasks

from .utils.fileHandler import FileHandler


class Accounting(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.find_member_not_exists_in_db.start()

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

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        try:
            exists = (
                True
                if await FileHandler().ReadFile(f"accounting/{member.id}.json")
                else True
            )
        except FileNotFoundError:
            exists = False

        if not exists:
            await FileHandler().SaveFile(
                f"accounting/{member.id}.json", {"money": 20000}
            )  # 20k for joining
            await member.send(
                embed=discord.Embed(
                    title="New user detected!",
                    description="Hello there! You're now getting 20000 coins as a welcome gift!\nGamble wisely and don't ever get yourself in debt!",
                )
            )

    @tasks.loop(hours=24)
    async def find_member_not_exists_in_db(self) -> None:
        for member in self.bot.get_all_members():
            try:
                exists = (
                    True
                    if FileHandler().ReadFile(f"accounting/{member.id}.json")
                    else True
                )
            except FileNotFoundError:
                exists = False

            if not exists:
                FileHandler().SaveFile(
                    f"accounting/{member.id}.json",
                    {"money": 20000},
                )

    @account.command()
    async def balance(self, ctx: commands.Context, member: discord.User = None):
        target = member if member else ctx.author
        h = await FileHandler().ReadFile(f"accounting/{target.id}.json")
        await ctx.send(
            embed=(
                (
                    discord.Embed(
                        title=f"{str(target)}'s account balance",
                    )
                )
            )
            .add_field(name="Balance", value=h["balance"])
            .add_field(name="Debt", value=h["debt"])
        )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Accounting(bot))
