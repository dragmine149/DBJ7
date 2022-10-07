import discord
import typing
from .utils import bank as bank, uis as uis
from _typeshed import Incomplete
from discord.ext import commands

class game_loader(commands.Cog):
    @property
    def display_emoji(self) -> typing.Union[str, bytes, discord.PartialEmoji]: ...
    bot: Incomplete
    game_module: Incomplete
    games: Incomplete
    module_names: Incomplete
    logger: Incomplete
    chosenGame: str
    msg: Incomplete
    def __init__(self, bot: commands.bot) -> None: ...
    async def game_select(self, Interaction: discord.Interaction, values: list[str]): ...
    async def game_cancel(self, Interaction: discord.Interaction): ...
    async def game_premethod(self, Interaction: discord.Interaction, label: str): ...
    confirmInteract: Incomplete
    async def game_preLoad(self, Interaction: discord.Interaction, data: list[str]): ...
    async def process_gameInput(self, ctx: commands.Context, game: typing.Optional[str]) -> bool: ...
    account: Incomplete
    async def playgame(self, ctx: commands.Context, game: typing.Optional[str]): ...
    def reload_game(self, module: str) -> str: ...
    def reload_games(self, module: Incomplete | None = ...) -> str: ...
    async def reloadgames(self, ctx: commands.Context, module: typing.Optional[str] = ...): ...

async def setup(bot: commands.Bot) -> None: ...
