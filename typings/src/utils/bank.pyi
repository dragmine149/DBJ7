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
    def to_dict(self): ...
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
    @classmethod
    async def get_by_id(cls, user_id: int) -> Player_Status: ...
    @classmethod
    async def initialize_new_user(cls, user_id: int) -> Player_Status: ...
    @staticmethod
    async def get_users() -> typing.List[int]: ...
    @property
    def to_dict(self): ...
    def __setattr__(self, __name: str, __value: typing.Any) -> None: ...
    def __init__(self, user, money, debt, unlucky, last_paid_debt, wins, loses, additional_data, inventory) -> None: ...
