import dataclasses
import logging
import typing
from datetime import date, datetime
import discord
from discord.ext import commands

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

    user: discord.User
    money: int
    debt: typing.Optional[int]
    unlucky: typing.Union[int, float, None] = 0
    last_paid_debt : typing.Union[datetime,None] = None

    def __str__(self) -> str:
        return f"{self.user} has {self.money} coins and in debt of {self.debt} coins and have unluckiness percent of {self.unlucky}%"

    @classmethod
    async def get_by_id(cls, user_id: int) -> "Player_Status":
        try:
            data = await FileHandler().ReadFile(f"accounting/{user_id}.json")
        except FileNotFoundError:
            data = {"money": 20000, "debt": 0, "unlucky": 0, "user": user_id,"last_paid_debt": None}
            await FileHandler().SaveFile(f"accounting/{user_id}.json", data)
        return cls(
            discord.utils.get(bot.users, id=user_id),
            data["money"],
            data["debt"],
            data["unlucky"],
            datetime.fromtimestamp(data["last_paid_debt"]) if data["last_paid_debt"] else None
        )

    @classmethod
    async def initialize_new_user(cls, user_id: int):
        data = {"money": 20000, "debt": 0, "unlucky": 0, "user": user_id, "last_paid_debt": None}
        await FileHandler().SaveFile(f"accounting/{user_id}.json", data)
        return cls(
            discord.utils.get(bot.users, id=user_id),
            data["money"],
            data["debt"],
            data["unlucky"],
            None
        )

    def __setattr__(self, __name: str, __value: typing.Any) -> None:
        if __name == "money":
            if __value < 0:
                raise ValueError("Money cannot be negative")
            bot.loop.create_task(
                FileHandler().SaveFile(
                    f"accounting/{self.user.id}.json",
                    {"money": __value, "debt": self.debt, "unlucky": self.unlucky, "user": self.user.id,"last_paid_debt":self.last_paid_debt.timestamp() if self.last_paid_debt else None},
                )
            )
        elif __name == "debt":
            if __value < 0:
                raise ValueError("Debt cannot be negative")
            bot.loop.create_task(
                FileHandler().SaveFile(
                    f"accounting/{self.user.id}.json",
                    {"money": self.money, "debt": __value, "unlucky": self.unlucky, "user": self.user.id,"last_paid_debt":self.last_paid_debt.timestamp() if self.last_paid_debt else None},
                )
            )
        elif __name == "unlucky":
            if __value < 0:
                raise ValueError("Unlucky cannot be negative")
            bot.loop.create_task(
                FileHandler().SaveFile(
                    f"accounting/{self.user.id}.json",
                    {"money": self.money, "debt": self.debt, "unlucky": __value, "user": self.user.id,"last_paid_debt":self.last_paid_debt.timestamp() if self.last_paid_debt else None},
                )
            )
        elif __name == "last_paid_debt":
            bot.loop.create_task(
                FileHandler().SaveFile(
                    f"accounting/{self.user.id}.json",
                    {
                        "money": self.money,
                        "debt": self.debt,
                        "unlucky": self.unlucky,
                        "user": self.user.id,
                        "last_paid_debt": __value.timestamp() if __value else None,
                    }
                )
            )
        setattr(self, __name, __value)
