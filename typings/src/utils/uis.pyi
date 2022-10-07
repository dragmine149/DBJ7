import discord
import typing
from _typeshed import Incomplete
from discord import ui

logger: Incomplete

class Button(ui.Button):
    callbackFunc: Incomplete
    clicked: bool
    def __init__(self, label: typing.Optional[str], callback: Incomplete | None = ..., **kwargs) -> None: ...
    async def callback(self, Interaction: discord.Interaction): ...
    async def defaultCallBack(self, Interaction: discord.Interaction, label: str): ...

class Multiple_Buttons(ui.View):
    def __init__(self, data=...) -> None: ...
    components: typing.List[Button]
    def Add_Button(self, label: typing.Optional[str], callback: Incomplete | None = ..., **kwargs) -> None: ...
    @property
    def choosen(self) -> Button: ...
    def Edit_Button(self, index, **kwargs) -> None: ...

class Dropdown(ui.Select):
    callbackFunc: Incomplete
    def __init__(self, callback: Incomplete | None = ..., **kwargs) -> None: ...
    async def callback(self, interaction: discord.Interaction): ...
    async def defaultCallback(self, interaction: discord.Interaction, values: list[str]): ...

class DropdownView(ui.View):
    def __init__(self, callback: Incomplete | None = ..., **kwargs) -> None: ...
    def add_dropdown(self, callback: Incomplete | None = ..., **kwargs) -> None: ...