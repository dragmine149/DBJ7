import discord
import typing
from .fileHandler import FileHandler as FileHandler
from _typeshed import Incomplete
from datetime import datetime
from discord.ext import commands as commands

logger: Incomplete
bot: typing.Optional[commands.Bot]

def __getattr__(name: str) -> typing.Any: ...

class Inventory:
    items: typing.Dict[str, int]
    @property
    def to_dict(self) -> dict[str, typing.Dict[str, int]]: ...
    def __init__(self, items) -> None: ...

class Effect:
    effect_name: str
    effect_lucky_multiplier: float
    effect_unlucky_multiplier: float
    coin_multiplier: float
    expire_time: datetime
    game_name: str
    def activate(self, game_name: Incomplete | None = ...) -> None: ...
    @classmethod
    def coin_multiplier(cls, coin_multiplier: float): ...
    @classmethod
    def lucky_potion(cls): ...
    @classmethod
    def fake_lucky_potion(cls): ...
    @classmethod
    def wipe_effect(cls): ...
    def __init__(self, effect_name, effect_lucky_multiplier, effect_unlucky_multiplier, coin_multiplier, expire_time, game_name) -> None: ...

class Effects:
    effects: typing.List[Effect]
    @property
    def to_dict(self) -> dict[str, typing.Dict[str, int]]: ...
    def __init__(self, effects) -> None: ...

class Player_Status:
    user: discord.User
    money: int
    debt: typing.Optional[int]
    unlucky: typing.Union[int, float, None]
    last_paid_debt: typing.Union[datetime, None]
    wins: int
    loses: int
    additional_data: typing.Optional[typing.Dict[str, typing.Any]]
    inventory: Inventory
    effects: Effects
    @classmethod
    async def get_by_id(cls, user_id: int) -> Player_Status: ...
    @classmethod
    async def initialize_new_user(cls, user_id: int) -> Player_Status: ...
    @staticmethod
    async def get_users() -> typing.List[int]: ...
    @property
    def to_dict(self): ...
    def __setattr__(self, __name: str, __value: typing.Any) -> None: ...
    async def save(self) -> None: ...
    def __init__(self, user, money, debt, unlucky, last_paid_debt, wins, loses, additional_data, inventory, effects) -> None: ...
