
import discord
from discord.ext import commands

from utils import uis
import random
import aenum

class Coin_State(aenum.MultiValueEnum):
    head = 1, "head"
    tail = 0, "tail"
    
    def __str__(self):
        return self.name

class FlipCoin:
    """
    Flip a coin, bet on what side it lands on
    """

    def __init__(self, bot: commands.cog) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> str:
        return "🪙"

    async def start(self, Interaction: discord.Interaction):
        await Interaction.response.send_message("Loading game data...")
        # TODO: have a button ui to let the user select the amount of money they want to bet.
        await Interaction.edit_original_response(content="Please enter amount to bet")

        buttons = uis.Multiple_Items(
            [
                uis.Button(label="Head", emoji="🪙", style=discord.ButtonStyle.primary),
                uis.Button(label="Tail", emoji="🪙", style=discord.ButtonStyle),
            ]
        )
        await Interaction.edit_original_response(
            content="Please select an option", view=buttons
        )
        await buttons.wait()
        flip = Coin_State(random.randint(0, 1))
        response = Coin_State(buttons.check().lower())
        if flip == response:
            await Interaction.edit_original_response(
                content=f"You won! The coin landed on {str(flip)}"
            )
        else:
            await Interaction.edit_original_response(
                content=f"You lost! The coin landed on {str(flip)} while you choosed {str(response)}"
            )


def game_setup(bot):
    return FlipCoin(bot)
