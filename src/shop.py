import logging
from datetime import datetime

import discord
from discord.ext import commands, tasks

from .utils import bank
from .utils.enums import Items


class Inventory_And_Shop(commands.Cog, name="Inventory and shop"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_effects.start()
        self.log = logging.getLogger("bot.Inventory_And_Shop")

    @tasks.loop(minutes=1)
    async def check_effects(self):
        """
        Check if any effect has expired
        """
        for user in self.bot.users:
            if user.bot:
                continue
            account = await bank.Player_Status.get_by_id(user.id)
            for effect in account.effects:
                if not effect.expire_time:
                    continue
                if datetime.now() - effect.expire_time > datetime.timedelta(minutes=10):
                    account.effects.remove(effect)
                    logging.info(f"Effect {effect} has expired for {user}")

    @commands.hybrid_group()
    async def shop(self, ctx: commands.Context):
        """Shop commands"""

    @shop.command()
    async def buy(self, ctx: commands.Context, item: Items = None, amount: int = 1):
        """Buy an item"""
        await ctx.defer()
        account = await bank.Player_Status.get_by_id(ctx.author.id)
        if not item:
            embed = discord.Embed(title="Shop", description="Buy an item from the shop")
            for item in Items:
                embed.add_field(
                    name=item.name,
                    value=f"Price: {item.__price__} coins\nDescription: {item.__doc__}",
                )
            await ctx.send(embed=embed)
        money = amount * item.__price__
        if account.money < money:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Error",
                    description=f"You don't have enough coins to buy this item\nExpected: {money} coins\nActual: {account.money} coins",
                    color=discord.Color.red(),
                )
            )
        account.money -= money
        for x in range(amount):
            account.inventory.items.append(item.value)
        await ctx.reply(
            embed=discord.Embed(
                title="Success",
                description=f"You have bought {amount} {item.name} for {money} coins",
                color=discord.Color.green(),
            )
        )

    @shop.command()
    async def sell(self, ctx: commands.Context, item: Items, amount: int = 1):
        account = await bank.Player_Status.get_by_id(ctx.author.id)
        if item.value not in account.inventory.items:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Error",
                    description=f"You don't have this item in your inventory",
                    color=discord.Color.red(),
                )
            )
        if amount > account.inventory.items.count(item.value):
            return await ctx.reply(
                embed=discord.Embed(
                    title="Error",
                    description=f"You don't have enough of this item in your inventory",
                    color=discord.Color.red(),
                )
            )
        account.money += (amount * item.__price__) * 0.75
        await ctx.reply(
            embed=discord.Embed(
                title="Success",
                description=f"You have sold {amount} {item.name} for {amount * item.__price__ * 0.75} coins",
                color=discord.Color.green(),
            )
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Inventory_And_Shop(bot))
