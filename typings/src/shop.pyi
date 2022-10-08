import discord
from .utils import bank as bank
from .utils.enums import Items as Items
from _typeshed import Incomplete
from discord.ext import commands

class Inventory_And_Shop(commands.Cog):
    bot: Incomplete
    log: Incomplete
    def __init__(self, bot: commands.Bot) -> None: ...
    @property
    def display_emoji(self): ...
    async def check_effects(self) -> None: ...
    async def shop(self, ctx: commands.Context): ...
    async def list(self, ctx: commands.Context): ...
    async def buy(self, ctx: commands.Context, item: Items, amount: int = ...): ...
    async def sell(self, ctx: commands.Context, item: Items, amount: int = ...): ...
    async def send_money(self, ctx: commands.Context, user: discord.User, amount: int): ...
    async def inventory(self, ctx: commands.Context): ...
    async def list(self, ctx: commands.Context): ...
    async def use(self, ctx: commands.Context, item: Items, game_name: Incomplete | None = ...): ...
    async def effects(self, ctx: commands.Context): ...

async def setup(bot: commands.Bot): ...
