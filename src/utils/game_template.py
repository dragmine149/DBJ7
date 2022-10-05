import discord
from discord.ext import commands

from . import bank


class Template:
    """
    A game template
    """

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        bank.bot = bot
        self.bet: int = None
        self.interaction: discord.Interaction = None

    async def money_callback(self, value: int) -> None:
        raise NotImplemented

    async def start(self, interaction: discord.Interaction):
        raise NotImplemented