import discord
from _typeshed import Incomplete
from discord.ext import commands as commands
from src.utils import bank as bank, game_template as game_template, uis as uis
from src.utils.Cards import Cards as Cards
from src.utils.MoneySelector import MoneySelector as MoneySelector

logger: Incomplete

class HigherOrLower(game_template.Template):
    aliases: Incomplete
    modName: str
    bot: Incomplete
    currentCard: int
    correct: int
    view: Incomplete
    embed: Incomplete
    def __init__(self, bot: commands.Bot) -> None: ...
    @property
    def display_emoji(self) -> str: ...
    async def Finish(self) -> None: ...
    def GenerateEmbed(self) -> discord.Embed: ...
    async def GuessCallback(self, Interaction: discord.Interaction, label: str): ...
    async def HigherLower(self): ...
    betValue: Incomplete
    account: Incomplete
    async def money_callback(self, value: int, user): ...
    user: Incomplete
    Interaction: Incomplete
    card: Incomplete
    async def start(self, Interaction: discord.Interaction): ...

def game_setup(bot): ...
