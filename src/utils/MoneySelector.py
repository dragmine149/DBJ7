"""
Documentation
- A module meant to bring a way to add or remove an ammount of money by using simple buttons.

How To Import
-------------
from MoneySelector import MoneySelector

How to use
----------
- Create a new MoneySelector class, pass in an discord.Interaction object and (recommened) a function for the callback.
-- If no discord.Interaction, will break
-- If no callback, will use the default call back which doesn't return data.

- Call function `get_money()` this will do the rest
- The money that the user wants to input, will be set back in the callback function.

Callback Function
-----------------
- Requires 2 inputs
-- discord.Intercation
--- Even though it's the same interaction put into MoneySelector, is required for elsewhere.
--- Can only edit the response to this interaction.
-- int
--- This is the value of the amount selected
"""

import discord

from src.utils import uis


class MoneySelector:
    def __init__(self, Interaction: discord.Interaction, callback=None) -> None:
        """Choose an amount of money with a couple of buttons

        Args:
            Interaction (discord.Interaction): The interaction message to edit
            callback (_type_, optional): The function which gets callbacked once they are done with the input. Defaults to None.
        """
        self.Interaction = Interaction
        self.callback = callback
        if self.callback is None:
            self.callback = self.defaultCallBack

        self.value = 0

        self.view = uis.Multiple_Buttons(
            [
                {
                    "label": "+100",
                    "callback": self.changeValue,
                    "style": discord.ButtonStyle.primary,
                    "emoji": "💵",
                },
                {
                    "label": "+10",
                    "callback": self.changeValue,
                    "style": discord.ButtonStyle.primary,
                    "emoji": "💵",
                },
                {
                    "label": "+1",
                    "callback": self.changeValue,
                    "style": discord.ButtonStyle.primary,
                    "emoji": "💵",
                },
                {
                    "label": "-100",
                    "callback": self.changeValue,
                    "style": discord.ButtonStyle.danger,
                    "emoji": "💴",
                    "row": 1,
                },
                {
                    "label": "-10",
                    "callback": self.changeValue,
                    "style": discord.ButtonStyle.danger,
                    "emoji": "💴",
                    "row": 1,
                },
                {
                    "label": "-1",
                    "callback": self.changeValue,
                    "style": discord.ButtonStyle.danger,
                    "emoji": "💴",
                    "row": 1,
                },
                {
                    "label": "Confirm",
                    "callback": self.FinishedCallback,
                    "style": discord.ButtonStyle.success,
                    "emoji": "✅",
                    "row": 2,
                },
            ]
        )

    async def defaultCallBack(self, value):
        await self.Interaction.edit_original_response(f"You choice {value}")

    async def FinishedCallback(self, Interaction: discord.Interaction, label: str):
        await self.callback(self.value)

    async def changeValue(self, Interaction: discord.Interaction, label: str):
        money = int(label[1:])
        if label[0] == "+":
            self.value += money
        if label[0] == "-":
            self.value -= money

        await Interaction.response.send_message(
            content=f"Changed ammount betting by: {money}", ephemeral=True
        )
        await self.Interaction.edit_original_response(
            content=f"How much money do you want to bet? Currently betting: {self.value}",
            view=self.view,
        )

    async def show_message(self):
        await self.Interaction.edit_original_response(
            content=f"How much money do you want to bet? Currently betting: {self.value}",
            view=self.view,
        )

    async def get_money(self):
        await self.show_message()
