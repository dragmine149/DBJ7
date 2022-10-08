from discord.ext import commands
from .utils import bank
import random
from datetime import datetime
class Inventory_And_Shop(commands.Cog, name="Inventory and shop"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.hybrid_group()
    async def shop(self, ctx: commands.Context):
        """Shop commands"""
    
    @shop.command()
    async def buy(self, ctx: commands.Context, item: Items, amount: int):
        """Buy an item"""
    


async def setup(bot: commands.Bot):
    await bot.add_cog(Inventory_And_Shop(bot))
