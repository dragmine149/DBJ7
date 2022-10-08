import discord
import typing
from _typeshed import Incomplete
from discord.ext import commands as commands
from src.utils import bank as bank, game_template as game_template, uis as uis
from src.utils.MoneySelector import MoneySelector as MoneySelector

logger: Incomplete

class twentyOne(game_template.Template):
    modName: str
    aliases: typing.List
    betValue: int
    view: Incomplete
    score: int
    interaction: Incomplete
    def __init__(self, bot: commands.Bot) -> None: ...
    @property
    def display_emoji(self) -> str: ...
    async def PullOut(self, Interaction: discord.Interaction, label: str): ...
    async def rollDice(self, Interaction: discord.Interaction, label: str): ...
    async def show_ui(self): ...
    async def money_callback(self, value: int) -> None: ...
    Interaction: Incomplete
    account: Incomplete
    async def start(self, Interaction: discord.Interaction): ...

def game_setup(bot: commands.bot): ...
