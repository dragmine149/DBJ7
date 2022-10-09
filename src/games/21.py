import logging
import math
import random
import typing

import discord
from discord.ext import commands

from src.utils import bank, game_template, uis
from src.utils.MoneySelector import MoneySelector

logger = logging.getLogger("games.21")
logger.info("Initalised")


class twentyOne(game_template.Template):
    """Get as close to 21 as possible without going over"""

    modName = "21"
    aliases: typing.List = ["21"]

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.betValue = 0

        self.view = uis.Multiple_Buttons(
            [
                {
                    "label": "roll",
                    "callback": self.rollDice,
                    "style": discord.ButtonStyle.primary,
                },
                {
                    "label": "pull out",
                    "callback": self.PullOut,
                    "style": discord.ButtonStyle.danger,
                },
            ]
        )
        self.score = 0
        self.interaction: discord.Interaction

    @property
    def display_emoji(self) -> str:
        return "🔢"

    async def PullOut(self, Interaction: discord.Interaction, label: str):
        """Generate amount of money that is required for the time when they pulled out.

        Callculation:
        money = round(1 * self.score / math.pi / 0.01 * 69 / 10000, 3)
        - Complecated? yes
        - Why?: why not

        """
        if Interaction.user.id != self.interaction.user.id:
            return await Interaction.response.send_message(
                "You can not pull out for this user!", ephemeral=True
            )

        moneyMulti = round(1 * self.score / math.pi / 0.01 * 69 / 10000, 3)

        if self.score == 21:
            moneyMulti = round(moneyMulti, 1)
        if "coin_multiplier" in [
            x.effect_name
            for x in self.account.effects
            if x.effect_name == "coin_multiplier"
        ] and (
            not [x for x in self.account.effects if x.effect_name == "coin_multiplier"][
                0
            ].game_name
            or [x for x in self.account.effects if x.effect_name == "coin_multiplier"][
                0
            ].game_name.lower()
            == "flip_coin"
        ):
            for effect in self.account.effects:
                if effect.effect_name == "coin_multiplier":
                    break
            moneyMulti += effect.coin_multiplier
        moneyReward = int(self.betValue * moneyMulti)
        self.account.money += int(moneyReward)

        await Interaction.response.send_message(
            f"You pulled out at score: {self.score}", ephemeral=True
        )
        await self.Interaction.edit_original_response(
            content=f"Well done you earned {moneyReward} (Multiplayer: {moneyMulti})",
            view=None,
        )

    async def rollDice(self, Interaction: discord.Interaction, label: str):
        """Rolls a dice,
        If user is unlucky we want the dice roles to be higher the nearer they get to 21
        So, higher unlucky = higher role, i think
        """
        if Interaction.user.id != self.interaction.user.id:
            return await Interaction.response.send_message(
                "You can not roll a dice for this user!", ephemeral=True
            )

        unluckLimit = random.randrange(10)
        maxLimit = 1
        if self.score >= unluckLimit:
            maxLimit = random.randrange(1, 4)

        diceRole: float = random.randint(1, 6 * maxLimit)
        logger.debug(diceRole)
        logger.debug(maxLimit)

        if diceRole > 6:
            diceRole = diceRole % 1.005

        if diceRole < 1:
            diceRole = 1

        diceRole = int(diceRole)

        self.score += diceRole
        await Interaction.response.send_message(
            f"You rolled a {diceRole}.", ephemeral=True
        )
        await self.show_ui()

    async def show_ui(self):
        logger.debug("Showing ui")
        if (
            self.score > 21
        ):  # Only stop if they go over, don't warn them for anything else.
            return await self.Interaction.edit_original_response(
                content=f"You went over the limit and lost everything.", view=None
            )

        await self.Interaction.edit_original_response(
            content=f"Current value: {self.score}. What do you do?", view=self.view
        )

    async def money_callback(self, value: int) -> None:
        self.betValue = value
        self.account.money -= value
        await self.show_ui()

    async def start(self, Interaction: discord.Interaction):
        self.score = 0
        await Interaction.response.send_message("Loading game...")
        self.Interaction = Interaction

        self.account = await bank.Player_Status.get_by_id(Interaction.user.id)
        await MoneySelector(Interaction, self.money_callback).get_money()


def game_setup(bot: commands.bot):
    return twentyOne(bot)
