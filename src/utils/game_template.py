import typing

import discord
from discord.ext import commands

from src.utils import bank


class Template:
    """
    A game template
    """

    aliases: typing.List = []
    name: str = ""

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        bank.bot = bot
        self.bet: int = 0
        self.interaction: discord.Interaction = None  # type: ignore

    async def money_callback(self, value: int) -> None:
        raise NotImplemented

    async def start(self, interaction: discord.Interaction):
        raise NotImplemented
