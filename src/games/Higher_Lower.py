import asyncio
import logging

import discord
from discord.ext import commands

from src.utils import bank, game_template, uis
from src.utils.Cards import Cards
from src.utils.MoneySelector import MoneySelector

logger = logging.getLogger("game.Higher_Lower.log")
logger.info("Initalised")

# Probably don't need an unlucky factor for this game


class HigherOrLower(game_template.Template):
    """
    Guess higher or lower on a card value
    """

    aliases = ["HOL"]
    name = "Higher or Lower"

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        bank.bot = bot
        self.currentCard = 0
        self.correct = 0

        self.view = uis.Multiple_Buttons(
            [
                {
                    "label": "higher",
                    "callback": self.GuessCallback,
                    "emoji": "⬆️",
                    "style": discord.ButtonStyle.primary,
                },
                {
                    "label": "lower",
                    "callback": self.GuessCallback,
                    "emoji": "⬇️",
                    "style": discord.ButtonStyle.secondary,
                },
            ]
        )

        self.embed = discord.Embed(
            color=discord.Color.random(),
            title="Higher Lower Progress",
            description="Your progress report on this game",
        )

        self.embed.add_field(name="Current Card", value="")
        self.embed.add_field(name="Progress", value="")
        self.embed.add_field(name="Correct Guesses", value="")

    @property
    def display_emoji(self) -> str:
        return "↕️"

    async def Finish(self):
        """
        Finish looping through all cards, show end response
        """
        moneyMultiplier = 0.025 * self.correct
        moneyReward = self.betValue * moneyMultiplier

        self.account.money += moneyReward
        await self.Interaction.edit_original_response(
            content=f"You got a multiplier of {str(moneyMultiplier)[0:5]}x.\nFor a reward of {moneyReward}\n\nGame Information",
            embed=self.GenerateEmbed(),
            view=None,
        )

    def GenerateEmbed(self) -> discord.Embed:
        """Generate an embed with the current game progress and information

        Returns:
            discord.Embed: The embed that gets generated
        """
        cc = self.card.Get_Deck_Card(self.currentCard)
        self.embed.set_field_at(
            0, name=self.embed.fields[0].name, value=f"{cc[1]} of {cc[0]}"
        )

        self.embed.set_field_at(
            1,
            name=self.embed.fields[1].name,
            value=f"{str(round((self.currentCard + 1) / 52, 4) * 100)[0:5]}%",
        )

        self.embed.set_field_at(2, name=self.embed.fields[2].name, value=self.correct)

        return self.embed

    async def GuessCallback(self, Interaction: discord.Interaction, label: str):
        """Does some checks on their inputs, and other stuff"""
        if Interaction.user.id != self.user.id:
            return await Interaction.response.send_message(
                "You can not choose an option for this user!", ephemeral=True
            )

        # Check if they won that higher or lower
        self.currentCard += 1
        oldCard = self.card.Get_Deck_Card(self.currentCard - 1)
        nextCard = self.card.Get_Deck_Card(self.currentCard)
        higher = self.card.Check_If_Higher(oldCard, nextCard)
        highermsg = "higher" if higher else "lower"

        correctmsg = "Incorrect"
        if label == highermsg:
            self.correct += 1
            correctmsg = "Correct"

        # respond
        # await Interaction.response.defer()
        await Interaction.response.send_message(
            content=f"You were {correctmsg}, the new card is {highermsg} than the old card. Left: {52 - (self.currentCard + 1)}"
        )
        await self.HigherLower()
        await asyncio.sleep(1)
        await Interaction.delete_original_response()

    async def HigherLower(self):
        """Main loop"""
        if self.currentCard == 51:
            return await self.Finish()

        await self.Interaction.edit_original_response(
            content="", view=self.view, embed=self.GenerateEmbed()
        )

    async def money_callback(self, value: int):
        """Callback function after selecting amount of money"""
        self.betValue = value
        self.account = await bank.Player_Status.get_by_id(self.Interaction.user.id)

        self.account.money -= value
        await self.HigherLower()

    async def start(self, Interaction: discord.Interaction):
        self.user = Interaction.user
        self.Interaction = Interaction
        self.embed.set_author(
            name=self.user.display_name, icon_url=self.user.display_avatar.url
        )

        self.currentCard = 0
        self.correct = 0

        await Interaction.response.send_message("Loading game data...")
        self.card = Cards()  # new deck per game
        self.card.shuffle_cards(nUnique=True)
        await MoneySelector(Interaction, self.money_callback).get_money()


def game_setup(bot):
    return HigherOrLower(bot)
