from .utils import time as time, uis as uis
from _typeshed import Incomplete
from discord.ext import commands

class Stuff(commands.Cog):
    bot: Incomplete
    def __init__(self, bot) -> None: ...
    @property
    def display_emoji(self): ...
    async def cog_before_invoke(self, ctx: commands.Context): ...
    async def credits(self, ctx: commands.Context): ...
    async def ping(self, ctx: commands.Context): ...
    async def status(self, ctx: commands.Context): ...
    async def invite(self, ctx: commands.Context): ...
    async def raise_error(self, ctx: commands.Context): ...

async def setup(bot) -> None: ...
