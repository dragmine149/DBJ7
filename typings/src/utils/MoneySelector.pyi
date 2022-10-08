import discord
from _typeshed import Incomplete
from src.utils import bank as bank, uis as uis

class MoneySelector:
    Interaction: Incomplete
    owner: Incomplete
    userOnly: Incomplete
    callback: Incomplete
    value: int
    view: Incomplete
    fsSent: bool
    def __init__(
        self,
        Interaction: discord.Interaction,
        callback: Incomplete | None = ...,
        userOnly: bool = ...,
    ) -> None: ...
    async def confirmCallback(self, Interaction: discord.Interaction, label: str): ...
    async def defaultCallBack(self, value, user) -> None: ...
    betMsg: Incomplete
    async def FinishedCallback(self, Interaction: discord.Interaction, label: str): ...
    async def changeValue(self, Interaction: discord.Interaction, label: str): ...
    async def show_message(self) -> None: ...
    account: Incomplete
    async def get_money(self) -> None: ...
