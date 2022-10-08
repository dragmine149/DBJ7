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

from src.utils import bank, uis


class MoneySelector:
    def __init__(
        self, Interaction: discord.Interaction, callback=None, userOnly: bool = False
    ) -> None:
        """Choose an amount of money with a couple of buttons

        Args:
            Interaction (discord.Interaction): The interaction message to edit
            callback (_type_, optional): The function which gets callbacked once they are done with the input. Defaults to None.
            userOnly (bool): Whever to show the message only to the user
        """
        self.Interaction = Interaction
        self.owner = self.Interaction.user
        self.userOnly = userOnly
        self.callback = callback
        if self.callback is None:
            self.callback = self.defaultCallBack

        self.value = 0

        self.view = uis.Multiple_Buttons(
            [
                {
                    "label": "+all",
                    "callback": self.changeValue,
                    "style": discord.ButtonStyle.primary,
                    "emoji": "💵",
                },
                {
                    "label": "+1000",
                    "callback": self.changeValue,
                    "style": discord.ButtonStyle.primary,
                    "emoji": "💵",
                },
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
                    "label": "-all",
                    "callback": self.changeValue,
                    "style": discord.ButtonStyle.danger,
                    "emoji": "💴",
                    "row": 1,
                },
                {
                    "label": "-1000",
                    "callback": self.changeValue,
                    "style": discord.ButtonStyle.danger,
                    "emoji": "💴",
                    "row": 1,
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
        self.fsSent: bool = False

    async def confirmCallback(self, Interaction: discord.Interaction, label: str):
        if Interaction.user.id != self.owner.id:
            return await Interaction.response.send_message(
                "You are not allowed to confirm for the owner of this interaction",
                ephemeral=True,
            )

        if label == "yes":
            await self.betMsg.delete_original_response()
            if self.userOnly:
                await self.Interaction.edit_original_response(content="Finished, this can be dissmissed now (I can't manualy remove this message)", view=None)
                
            return await self.callback(self.value, self.Interaction.user)

        await Interaction.response.send_message(
            content="Please enter new amount of money", ephemeral=True
        )
        await self.betMsg.delete_original_response()
        return await self.get_money()

    async def defaultCallBack(self, value, user):
        await self.Interaction.edit_original_response(
            f"You choice {value}", ephermal=self.userOnly
        )

    async def FinishedCallback(self, Interaction: discord.Interaction, label: str):
        view = uis.Multiple_Buttons(
            [
                {
                    "label": "yes",
                    "callback": self.confirmCallback,
                    "style": discord.ButtonStyle.success,
                    "emoji": "✅",
                },
                {
                    "label": "no",
                    "callback": self.confirmCallback,
                    "style": discord.ButtonStyle.danger,
                    "emoji": "❎",
                },
            ]
        )

        self.betMsg = Interaction
        await Interaction.response.send_message(
            f"You are betting {self.value} coins. Are you sure?", view=view
        )

    async def changeValue(self, Interaction: discord.Interaction, label: str):
        if Interaction.user.id != self.owner.id:
            return await Interaction.response.send_message(
                "You are not allowed to change the value of this interaction!",
                ephemeral=True,
            )
        money = 0
        if label[1:] == "all":
            money = self.account.money
        else:
            money = int(label[1:])

        if label[0] == "+":
            if self.account.money < self.value + money:
                return await Interaction.response.send_message(
                    f"That bid was higher than your money that your currently have! Go get some money if you want to bid higher!\nMoney that you currently having: {self.account.money}\nAmount of money you going to bid: {self.value + money}",
                    ephemeral=True,
                )
            self.value += money
        if label[0] == "-":
            if self.value - money < 0:
                return await Interaction.response.send_message(
                    "You can't bid negative money!", ephemeral=True
                )
            self.value -= money

        await Interaction.response.send_message(
            content=f"Changed ammount betting by: {label[0]}{money}", ephemeral=True
        )
        await self.Interaction.edit_original_response(
            content=f"How much money do you want to bet? Currently betting: {self.value}coins\n\nYour limit: {self.account.money}coins",
            view=self.view,
        )

    async def show_message(self):
        if not self.userOnly:
            await self.Interaction.edit_original_response(
                content=f"How much money do you want to bet? Currently betting: {self.value}coins\n\nYour limit: {self.account.money}coins",
                view=self.view,
            )
        elif not self.fsSent:
            await self.Interaction.followup.send(
                content=f"How much money do you want to bet? Currently betting: {self.value}coins\n\nYour limit: {self.account.money}coins",
                view=self.view,
                ephemeral=True,
            )
            self.fsSent = True

    async def get_money(self):
        self.account = await bank.Player_Status.get_by_id(self.Interaction.user.id)
        await self.show_message()

        tO = await self.view.wait()
        if tO:
            await self.Interaction.edit_original_response(
                content="Timed out! Automatically canceled",
            )
