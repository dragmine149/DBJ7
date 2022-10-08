import dataclasses
import logging
import os
import random
import traceback
import typing
from datetime import datetime

import aenum
import discord
import orjson as json
from discord.ext import commands

from .fileHandler import FileHandler

bot: typing.Optional[commands.Bot] = None


@dataclasses.dataclass
class Effect:
    effect_name: str
    effect_lucky_multiplier: float
    effect_unlucky_multiplier: float
    coin_multiplier: float
    expire_time: datetime = None
    game_name: str = None

    def activate(self, game_name=None):
        """
        Helper function to activate an effect (by add expire and optionally restrict it to a game)
        """
        self.expire_time = datetime.now() + datetime.timedelta(minutes=10)
        self.game_name = game_name

    @classmethod
    def coin_multiplier(cls, coin_multiplier: float):
        """
        Create a coin multiplier effect
        """
        return cls("coin multiplier", 1, 1, coin_multiplier)

    @classmethod
    def lucky_potion(cls):
        """
        Create a lucky potion effect
        """
        return cls("lucky potion", random.randint(2, 4), 1, 1)

    @classmethod
    def wipe_effect(cls):
        """
        Create a wipe effect
        """
        return cls("wipe", 1, 1, 1)

    @property
    def to_dict(self):
        return {
            "effect_name": self.effect_name,
            "effect_lucky_multiplier": self.effect_lucky_multiplier,
            "effect_unlucky_multiplier": self.effect_unlucky_multiplier,
            "coin_multiplier": self.coin_multiplier,
            "expire_time": self.expire_time.timestamp() if self.expire_time else None,
            "game_name": self.game_name,
        }


@dataclasses.dataclass
class Inventory:
    items: typing.List[Effect] = dataclasses.field(default_factory=list)

    @property
    def to_dict(self) -> list[Effect]:
        return self.items


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
    loses: int = 0
    additional_data: typing.Optional[typing.Dict[str, typing.Any]] = None
    inventory: Inventory = None
    effects: typing.List[Effect] = dataclasses.field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.user} has {self.money} coins and in debt of {self.debt} coins and have unluckiness percent of {self.unlucky}%"

    @classmethod
    async def get_by_id(cls, user_id: int) -> "Player_Status":
        try:
            data = await FileHandler().ReadFile(f"{user_id}.json")
        except FileNotFoundError:
            return await cls.initialize_new_user(user_id)
        except json.JSONDecodeError:
            return await cls.initialize_new_user(user_id)

        try:
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
                Inventory([Effect(**item) for item in data["inventory"]]),
                [Effect(**effect) for effect in data["effects"]],
            )
        except KeyError:
            # Can we make this so it attempts to fix data instead of reseting data?
            # It probably shouldn't happen a lot but just in case, would be nice if we can fix before we reset.
            # I don't know, can we though?
            return await cls.initialize_new_user(user_id)
        except TypeError:
            # Going to assume that the data is broken, so once again remaking it.
            logger.error("Type error in returning data strucutre")
            logger.info(traceback.format_exc())
            return await cls.initialize_new_user(user_id)

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
            "inventory": [],
            "effects": [],
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
            Inventory([Effect(**effect) for effect in data["inventory"]]),
            [Effect(**effect) for effect in data["effects"]],
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
            "debt": self.debt,
            "effects": [effect.__dict__ for effect in self.effects],
        }

    def __setattr__(self, __name: str, __value: typing.Any) -> None:
        if __name == "user":
            self.__dict__[__name] = __value
        self.__dict__[__name] = __value
        bot.loop.create_task(self.save())

    async def save(self):
        data = self.to_dict
        copied = data.copy()
        for item in copied["inventory"]:
            if isinstance(item, dict):
                continue
            if isinstance(item, aenum.Enum):
                data["inventory"].remove(item)
                data["inventory"].append(item.value.to_dict)
            data["inventory"].remove(item)
            data["inventory"].append(item.to_dict)
        await FileHandler().SaveFile(f"{self.user.id}.json", data)
