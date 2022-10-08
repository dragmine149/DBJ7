import logging
import typing

import discord

from src.utils import uis
from src.utils.MoneySelector import MoneySelector

logger = logging.getLogger("src.utils.Multiplayer")
logger.info("Houston, we have a problem")


class Multiplayer:
    def __init__(self, Interaction: discord.Interaction, name: str, limit: int = 2):
        """Main class to support multiplayer.

        Args:
            Interaction (discord.Interaction): The interaction that originated the game
            limit (int, optional): How many people can play at once. Defaults to 2.
        """
        self.Interaction = Interaction
        self.owner = Interaction.user
        self.limit = limit

        self.data: typing.Dict[str, int] = {}
        self.game = name

    async def MoneyCallback(self, value: int, user: discord.Member):
        self.data[str(user.id)] = value

    async def AskCallback(self, Interaction: discord.Interaction, label: str):
        if label == "yes":
            await self.Invite(Interaction, label)
        if label == "no":
            await self.callback()

    async def Ask(self):
        """Ask the user if they want to play multiplayer"""
        multiplayer = uis.Multiple_Buttons(
            [
                {
                    "label": "yes",
                    "callback": self.AskCallback,
                    "style": discord.ButtonStyle.primary,
                    "emoji": "✅",
                },
                {
                    "label": "no",
                    "callback": self.AskCallback,
                    "style": discord.ButtonStyle.danger,
                    "emoji": "❎",
                },
            ]
        )

        try:
            await self.Interaction.response.send_message(
                f"Do you want to play with other people?", view=multiplayer
            )
        except discord.errors.InteractionResponded:
            await self.Interaction.edit_original_response(
                content=f"Do you want to play with other people?", view=multiplayer
            )

    async def AcceptInvitation(self, Interaction: discord.Interaction, label: str):
        """Accept a game invitation that someone through out in that channel"""

        # Checks if you haven't already accepted it
        try:
            self.data[str(Interaction.user.id)]
            await Interaction.response.send_message(
                "You have already joined this game", ephemeral=True
            )
            return
        except KeyError:
            pass

        # Checks if the game is not full
        if len(self.data) < self.limit:

            # Adds to the list
            self.data[str(Interaction.user.id)] = -10
            if len(self.data) == self.limit:
                self.buttonView.stop()

            await Interaction.response.send_message(
                "Joined game!\n\nPlease choose amount of money to bet", ephemeral=True
            )
            ms = MoneySelector(Interaction, self.MoneyCallback, userOnly=True)
            await ms.get_money()
        else:
            # Notifies user
            await Interaction.response.send_message(
                "Sorry but this game is full currently.", ephemeral=True
            )
            await self.InviteMsg.delete_original_response()
            self.buttonView.stop()  # stop after max people

    async def Invite(self, Interaction: discord.Interaction, label: str):
        """Opens a global invite for anyone who can see that channel to join."""
        self.buttonView = uis.Multiple_Buttons(
            [
                {
                    "label": "Play!",
                    "callback": self.AcceptInvitation,
                    "style": discord.ButtonStyle.primary,
                }
            ]
        )

        self.InviteMsg = Interaction
        await Interaction.response.send_message(
            f"Press the button to play with: {self.owner.mention} in {self.game}",
            view=self.buttonView,
        )
        await self.callback()

    async def callback(self):
        """Waits for information before sending back data

        Returns:
            Inforamtion: Calls the function inputed.
        """
        await self.buttonView.wait()

        waiting_for = []
        for person in self.data:
            if self.data[person] == -10:
                waiting_for.append(person)

        msg = "Waiting for:"
        for person in waiting_for:
            msg += f"\n <@{person}>"

        msg += "\nTo place a bet"

        await self.Interaction.edit_original_response(msg)

        if self.callbackFunc is None:
            logger.error("cbk is set to none! Can't return data")
        await self.callbackFunc(self.Interaction, self.data)

    async def start(self, callback=None):
        """This gets called for multiplayer support

        Args:
            callback (Function, optional): The function to call after e. Defaults to None. Function required args: (Interaction: discord.Interaction, Data:Data)
        """
        await self.Ask()
        self.callbackFunc = callback
