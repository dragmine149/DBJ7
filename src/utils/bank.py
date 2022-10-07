import dataclasses
import logging
import os
import typing
from datetime import datetime

import discord
from discord.ext import commands

try:
    import orjson as json
except ImportError:
    import json  # type: ignore

from .fileHandler import FileHandler
import asyncio

logger = logging.getLogger("bot.src.utils.bank")

bot: typing.Optional[commands.Bot] = None


def __getattr__(name: str) -> typing.Any:
    if name == "bot":
        if bot is None:
            raise AttributeError("bot is not set")
        return bot
    return globals()[name]


@dataclasses.dataclass
class Inventory:
    items: typing.Dict[str, int] = dataclasses.field(default_factory=dict)

    @property
    def to_dict(self) -> dict[str, typing.Dict[str, int]]:
        return {
            "items": self.items
        }
@dataclasses.dataclass
class Player_Status:
    """
    Player status class (a very fancy way to access player status)
    Also save values on modify :pausechamp:
    """

    user: discord.User = 0  # type: ignore
    money: int = 0
    debt: typing.Optional[int] = 0
    unlucky: typing.Union[int, float, None] = 0
    last_paid_debt: typing.Union[datetime, None] = None
    wins: int = 0
    loses:int = 0
    additional_data: typing.Optional[typing.Dict[str,typing.Any]] = None
    inventory: Inventory = Inventory()
    def __str__(self) -> str:
        return f"{self.user} has {self.money} coins and in debt of {self.debt} coins and have unluckiness percent of {self.unlucky}%"

    @classmethod
    async def get_by_id(cls, user_id: int) -> "Player_Status":
        try:
            data = await FileHandler().ReadFile(f"{user_id}.json")
        except FileNotFoundError:
            logger.warning(f"File not found for {user_id}. Creating new user")
            return await cls.initialize_new_user(user_id)
        except json.JSONDecodeError:
            logger.error(f"json data saved incorrectly! Resting user {user_id} data!")
            return await cls.initialize_new_user(user_id)

        return cls(
            discord.utils.get(bot.users, id=user_id),
            data["money"],
            data["debt"],
            data["unlucky"],
            datetime.fromtimestamp(data["last_paid_debt"])
            if data["last_paid_debt"]
            else None,
            data["wins"],
            data["loses"],
            data["additional_data"],
            Inventory(data["inventory"]),
        )

    @classmethod
    async def initialize_new_user(cls, user_id: int) -> "Player_Status":
        data = {
            "money": 20000,
            "debt": 0,
            "unlucky": 0,
            "user": user_id,
            "last_paid_debt": None,
            "wins": 0,
            "loses": 0,
            "additional_data": {},
            "inventory": {},
        }
        await FileHandler().SaveFile(f"{user_id}.json", data)
        return cls(
            discord.utils.get(bot.users, id=user_id),
            data["money"],
            data["debt"],
            data["unlucky"],
            None,
            data["wins"],
            data["loses"],
            data["additional_data"],
            Inventory(data["inventory"]),
        )

    @staticmethod
    async def get_users() -> typing.List[int]:
        return (int(x[:-5]) for x in os.listdir("Data/"))

    @property
    def to_dict(self):
        return {
            "user": self.user.id,
            "money": self.money,
            "unlucky": self.unlucky,
            "last_paid_debt": self.last_paid_debt.timestamp()
            if self.last_paid_debt
            else None,
            "wins": self.wins,
            "loses": self.loses,
            "additional_data": self.additional_data,
            "inventory": self.inventory.to_dict,
            "debt": self.debt
        }

    def __setattr__(self, __name: str, __value: typing.Any) -> None:
        if __name == "user":
            self.__dict__[__name] = __value
        logger.info(
            f"Transaction triggered from {self.user} to {__name} with value of {__value}"
        )
        self.__dict__[__name] = __value
        bot.loop.create_task(
            self.save()
        )
    async def save(self):
        data = self.to_dict
        await FileHandler().SaveFile(f"{self.user.id}.json",data)
        