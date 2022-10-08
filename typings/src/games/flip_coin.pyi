import discord
from _typeshed import Incomplete
from discord.ext import commands as commands
from src.utils import bank as bank, game_template as game_template, uis as uis
from src.utils.MoneySelector import MoneySelector as MoneySelector
from src.utils.Multiplayer import Multiplayer as Multiplayer
from src.utils.enums import Coin_State as Coin_State, Items as Items

logger: Incomplete

class FlipCoin(game_template.Template):
    multiplayer: bool
    modName: str
    aliases: Incomplete
    bot: Incomplete
    def __init__(self, bot: commands.cog) -> None: ...
    @property
    def display_emoji(self) -> str: ...
    def flip_coin(self, unlucky: float = ..., user_guess: Coin_State = ...) -> bool: ...
    account: Incomplete
    async def on_button_click(self, Interaction: discord.Interaction, label: str): ...
    betValue: Incomplete
    async def money_callback(self, value: int, user): ...
    choosen: Incomplete
    async def pre_game(self) -> None: ...
    async def MultiCallback(self, Interaction: discord.Interaction, data): ...
    user: Incomplete
    Interaction: Incomplete
    mp: Incomplete
    async def start(self, Interaction: discord.Interaction): ...

def game_setup(bot): ...
