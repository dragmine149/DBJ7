import asyncio
import logging
import discord
from discord.ext import commands

import random
from src.utils import uis
from src.utils.MoneySelector import MoneySelector

logger = logging.getLogger("games.flip_coin.log")
logger.info("Initalised")

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

    def flip_coin(self, unlucky: float = 0.01):
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
            logger.warning(f"{self.user.name} ({self.user.id}) has a unlucky percent of < 0.01 (very lucky) automatically set to 0.01!")
        
        land = random.randint(1, 2 * int(unlucky * 100))
        return land == 1
    
    async def on_button_click(self, Interaction: discord.Interaction, label: str):
        result = self.flip_coin(0.01)  # will change to unlucky percent meter
        options = ["Heads", "Tails"]
        coins = self.betValue
        await Interaction.response.send_message("Flipping...", ephemeral=True)
        await asyncio.sleep(1.5)
        
        if result:
            await self.Interaction.edit_original_response(content=f"It landed on {label}! You gained {coins} coins", view=None)
            # add coins
        else:
            options.pop(options.index(label))  # remove our selected one from the list
            await self.Interaction.edit_original_response(content=f"Oh oh, it landed on {options[0]}, you lost {coins} coins", view=None)
            # remove coins
        
    async def money_callback(self, value):
        self.betValue = value
        await self.pre_game()

    async def pre_game(self):
        # Do this in another function, so that we don't skip over the money input, although is there a better way to do this?

        # await self.Interaction.edit_original_response(content=bank.Player_Status(self.Interaction.user.id))

        view = uis.Multiple_Buttons()
        view.Add_Button("Heads", self.on_button_click,
                        style=discord.ButtonStyle.primary)
        view.Add_Button("Tails", self.on_button_click,
                        style=discord.ButtonStyle.primary)

        await self.Interaction.edit_original_response(content="Please select an option", view=view)

    async def start(self, Interaction: discord.Interaction):
        self.user = Interaction.user
        self.Interaction = Interaction
        
        await Interaction.response.send_message("Loading game data...")
        await MoneySelector(Interaction, self.money_callback).get_money()
        

def game_setup(bot):
    return FlipCoin(bot)
