from datetime import datetime

import discord
from discord.ext import commands, tasks

from .utils import bank
from .utils.enums import Items


class Inventory_And_Shop(commands.Cog, name="Inventory and shop"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @tasks.loop(minutes=1)
    async def check_effects(self):
        """
        Check if any effect has expired
        """
        for user in self.bot.users:
            account = await bank.Player_Status.get_by_id(user.id)
            for effect in account.effects:
                if datetime.now() - effect.expire_time > datetime.timedelta(minutes=10):
                    account.effects.remove(effect)

    @commands.hybrid_group()
    async def shop(self, ctx: commands.Context):
        """Shop commands"""

    @shop.command()
    async def buy(self, ctx: commands.Context, item: Items = None, amount: int = 1):
        """Buy an item"""
        await bank.Player_Status.get_by_id(ctx.author.id)
        if not item:
            embed = discord.Embed(title="Shop", description="Buy an item from the shop")
            for item in Items:
                embed.add_field(
                    name=item.name,
                    value=f"Price: {item.__price__} coins\nDescription: {item.__doc__}",
                )
            await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Inventory_And_Shop(bot))
