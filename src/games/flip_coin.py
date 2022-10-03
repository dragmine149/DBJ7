from click import style
from discord.ext import commands
import discord
# import random
# from utils import uis

class FlipCoin:
    """
    Flip a coin, bet on what side it lands on
    """

    def __init__(self, bot: commands.cog) -> None:
        self.bot = bot
        pass
    
    @property
    def display_emoji(self) -> str:
        return "🪙"

    async def start(self, Interaction: discord.Interaction):
        await Interaction.response.send_message("Loading game data...")
        # TODO: have a button ui to let the user select the amount of money they want to bet.
        await Interaction.edit_original_response(content="Please enter amount to bet")
        
        # buttons = uis.Multiple_Items([
        #     {
        #         "label":"Heads",
        #         "style":"primary",
        #         "emoji":"🧕"
        #     },
        #     {
        #         "label": "Tails",
        #         "style": "primary",
        #         "emoji": "🪙"
        #     }
        # ])
        
        # await Interaction.edit_original_response(content="Please select an option", view=buttons)
        

def game_setup(bot):
    return FlipCoin(bot)