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

logger = logging.getLogger("bot.src.utils.bank")

bot: typing.Optional[commands.Bot] = None


def __getattr__(name: str) -> typing.Any:
    if name == "bot":
        if bot is None:
            raise AttributeError("bot is not set")
        return bot
    return globals()[name]


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
        )

    @classmethod
    async def initialize_new_user(cls, user_id: int) -> "Player_Status":
        data = {
            "money": 20000,
            "debt": 0,
            "unlucky": 0,
            "user": user_id,
            "last_paid_debt": None,
        }
        await FileHandler().SaveFile(f"{user_id}.json", data)
        return cls(
            discord.utils.get(bot.users, id=user_id),
            data["money"],
            data["debt"],
            data["unlucky"],
            None,
        )

    @staticmethod
    async def get_users() -> typing.List[int]:
        return (int(x[:-5]) for x in os.listdir("Data/"))

    def __setattr__(self, __name: str, __value: typing.Any) -> None:
        logger.info(
            f"Transaction triggered from {self.user} to {__name} with value of {__value}"
        )
        if __name == "money":
            if __value < 0:
                raise ValueError("Money cannot be negative")
            bot.loop.create_task(
                FileHandler().SaveFile(
                    f"{self.user.id}.json",
                    {
                        "money": __value,
                        "debt": self.debt,
                        "unlucky": self.unlucky,
                        "user": self.user.id,
                        "last_paid_debt": self.last_paid_debt.timestamp()
                        if self.last_paid_debt
                        else None,
                    },
                )
            )
        elif __name == "debt":
            if __value < 0:
                raise ValueError("Debt cannot be negative")
            bot.loop.create_task(
                FileHandler().SaveFile(
                    f"{self.user.id}.json",
                    {
                        "money": self.money,
                        "debt": __value,
                        "unlucky": self.unlucky,
                        "user": self.user.id,
                        "last_paid_debt": self.last_paid_debt.timestamp()
                        if self.last_paid_debt
                        else None,
                    },
                )
            )
        elif __name == "unlucky":
            if __value < 0:
                raise ValueError("Unlucky cannot be negative")
            if __value > 1:
                raise ValueError("Unlucky can't be over than 1")
            bot.loop.create_task(
                FileHandler().SaveFile(
                    f"{self.user.id}.json",
                    {
                        "money": self.money,
                        "debt": self.debt,
                        "unlucky": __value,
                        "user": self.user.id,
                        "last_paid_debt": self.last_paid_debt.timestamp()
                        if self.last_paid_debt
                        else None,
                    },
                )
            )
        elif __name == "last_paid_debt":
            bot.loop.create_task(
                FileHandler().SaveFile(
                    f"{self.user.id}.json",
                    {
                        "money": self.money,
                        "debt": self.debt,
                        "unlucky": self.unlucky,
                        "user": self.user.id,
                        "last_paid_debt": __value.timestamp() if __value else None,
                    },
                )
            )
        self.__dict__[__name] = __value
