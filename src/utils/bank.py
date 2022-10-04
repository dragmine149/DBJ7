import dataclasses
import logging
import typing

import discord
from discord.ext import commands

from .fileHandler import FileHandler

logger = logging.getLogger("bot.src.utils.bank")

bot: typing.Optional[commands.Bot] = None


@dataclasses.dataclass
class Balance:
    user: discord.User
    money: int
    debt: typing.Optional[int]

    def __str__(self) -> str:
        return f"{self.user} has {self.money} coins and in debt of {self.debt} coins"

    @classmethod
    async def get_balance_by_user_id(cls, user_id: int) -> "Balance":
        data = await FileHandler().ReadFile(f"accounting/{user_id}.json")
        return cls(
            discord.utils.get(bot.users, id=user_id), data["money"], data["debt"]
        )


async def add_money(user_id: int, amount: int) -> bool:
    try:
        await FileHandler().SaveFile(f"accounting/{user_id}.json", {"money": 20000})
        logger.info(f"Added {amount} to {user_id}")
        return True
    except Exception:
        logger.exception("Failed to add money to user")
        return False


async def remove_money(user_id: int, amount: int) -> bool:
    try:
        await FileHandler().SaveFile(f"accounting/{user_id}.json", {"money": 20000})
        logger.info(f"Removed {amount} from {user_id}")
        return True
    except Exception:
        logger.exception("Failed to remove money from user")
        return False


async def get_money(user_id: int) -> Balance:
    try:
        return Balance(await FileHandler().ReadFile(f"accounting/{user_id}.json"))
    except FileNotFoundError:
        await FileHandler().SaveFile(
            f"accounting/{user_id}.json",
            {"user": user_id, "money": 20000, "debt": 0, "unlucky": 0},
        )
