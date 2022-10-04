import asyncio
import logging
import random

import aenum
import discord
from discord.ext import commands

from src.utils import bank, uis
from src.utils.MoneySelector import MoneySelector

logger = logging.getLogger("games.flip_coin.log")
logger.info("Initalised")


class Coin_State(aenum.MultiValueEnum):
    heads = 1, "heads"
    tails = 0, "tails"

    def __str__(self):
        return self.name


class FlipCoin:
    """
    Flip a coin, bet on what side it lands on
    """

    def __init__(self, bot: commands.cog) -> None:
        """_summary_

        Args:
            bot (commands.cog): _description_
        """
        self.bot = bot

    @property
    def display_emoji(self) -> str:
        return "🪙"

    def flip_coin(self, unlucky: float = 0.01, user_guess: Coin_State = None) -> bool:
        """
        How this works:
        ---------------

        The user input is always `1` no matter what they choose.
        The other value `2` is multiplied by their unlucky meter, giving a bigger chance for it to be more on what they didn't choose.
        We can always force this unlucky meter to be 1 if we want them to have a 50/50 chance.
        The unlucky percent is a float so that it can be times by 100.

        Args:
            unlucky (float): The unlucky percent of the user, this has to be a decimal number.
        """
        if unlucky < 0.01:
            unlucky = 0.01
            logger.warning(
                f"{self.user.name} ({self.user.id}) has a unlucky percent of < 0.01 (very lucky) automatically set to 0.01!"
            )

        if user_guess == Coin_State.heads:
            return (
                random.choices(
                    [Coin_State.heads, Coin_State.tails], weights=[1, 1 * (unlucky)]
                )[0]
                == Coin_State.heads
            )
        else:
            return (
                random.choices(
                    [Coin_State.heads, Coin_State.tails], weights=[1 * unlucky, 1]
                )[0]
                == Coin_State.tails
            )

    async def on_button_click(self, Interaction: discord.Interaction, label: str):
        self.account = await bank.Player_Status.get_by_id(Interaction.user.id)
        result = self.flip_coin(self.account.unlucky, Coin_State[label.lower()])
        options = ["Heads", "Tails"]
        coins = self.betValue
        await Interaction.response.send_message("Flipping...", ephemeral=True)
        await asyncio.sleep(1.5)
        if result:
            await self.Interaction.edit_original_response(
                content=f"It landed on {label}! You gained {coins} coins", view=None
            )
            self.account.money += coins
        else:
            options.pop(options.index(label))  # remove our selected one from the list
            await self.Interaction.edit_original_response(
                content=f"Oh oh, it landed on {options[0]}, you lost {coins} coins",
                view=None,
            )
            self.account.money -= coins
        j = random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.01, 0.02, 0.03, 0.04, 0.05])
        if (j + self.account.unlucky) > 1:
            self.account.unlucky = 1
        else:
            self.account.unlucky += j

    async def money_callback(self, value: int):
        self.betValue = value
        await self.pre_game()

    async def pre_game(self):
        # Do this in another function, so that we don't skip over the money input, although is there a better way to do this?

        # await self.Interaction.edit_original_response(content=bank.Player_Status(self.Interaction.user.id))

        view = uis.Multiple_Buttons()
        view.Add_Button(
            "Heads", self.on_button_click, style=discord.ButtonStyle.primary
        )
        view.Add_Button(
            "Tails", self.on_button_click, style=discord.ButtonStyle.primary
        )

        await self.Interaction.edit_original_response(
            content="Please select an option", view=view
        )
        await view.wait()
        self.choosen = Coin_State(view.choosen.label.lower())

    async def start(self, Interaction: discord.Interaction):
        self.user = Interaction.user
        self.Interaction = Interaction

        await Interaction.response.send_message("Loading game data...")
        await MoneySelector(Interaction, self.money_callback).get_money()


def game_setup(bot):
    return FlipCoin(bot)
