import discord
import typing
from _typeshed import Incomplete
from discord.ext import commands as commands
from src.utils import bank as bank

class Template:
    aliases: typing.List
    bot: Incomplete
    bet: int
    interaction: Incomplete
    def __init__(self, bot: commands.Bot) -> None: ...
    async def money_callback(self, value: int) -> None: ...
    async def start(self, interaction: discord.Interaction): ...
