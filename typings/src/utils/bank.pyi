import discord
import typing
from .fileHandler import FileHandler as FileHandler
from _typeshed import Incomplete
from datetime import datetime
from discord.ext import commands as commands

bot: typing.Optional[commands.Bot]

class Effect:
    effect_name: str
    effect_lucky_multiplier: float
    effect_unlucky_multiplier: float
    coin_multiplier: float
    expire_time: datetime
    game_name: str
    def activate(self, game_name: Incomplete | None = ...) -> None: ...
    def __hash__(self) -> int: ...
    @classmethod
    def coin_multiplier_cls(cls, coin_multiplier: float): ...
    @classmethod
    def lucky_potion(cls): ...
    @classmethod
    def wipe_effect(cls): ...
    @property
    def to_dict(self): ...
    def __init__(self, effect_name, effect_lucky_multiplier, effect_unlucky_multiplier, coin_multiplier, expire_time, game_name) -> None: ...

class Inventory:
    items: typing.List[Effect]
    @property
    def to_dict(self) -> list[Effect]: ...
    def __init__(self, items) -> None: ...

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
    effects: typing.List[Effect]
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
