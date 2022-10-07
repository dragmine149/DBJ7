from _typeshed import Incomplete
from discord.ext import commands

class Shop(commands.Cog):
    bot: Incomplete
    def __init__(self, bot: commands.Bot) -> None: ...

async def setup(bot: commands.Bot): ...
