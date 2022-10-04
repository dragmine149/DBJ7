import importlib
import logging
import os
import typing

import discord
from discord.ext import commands

from .utils import uis


class game_loader(commands.Cog, name="Games"):
    """
    Play any game!
    """

    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.game_module = []
        self.games = []
        self.logger = logging.getLogger("bot.game")
        self.logger.info("initialized")

        for game in os.listdir("src/games"):
            if game.endswith(".py"):
                # Load all games, we do this to keep the game cogs seperate from the main discord bot.
                # Just makes everything better IMO.
                # Also means, we should be able to create new files without having to reload the bot

                module = importlib.import_module(f"src.games.{game[:-3]}")
                self.game_module.append(module)
                self.games.append(module.game_setup(self.bot))
                self.logger.info(f"Loaded {game} into game_loader")

    @property
    def display_emoji(self) -> typing.Union[str, bytes, discord.PartialEmoji]:
        return "🎮"

    async def game_select(self, Interaction: discord.Interaction, values: list[str]):
        for game in self.games:
            if type(game).__name__ == values[0]:
                try:
                    # await self.msg.delete()  # Don't know whever to delete original message or not
                    await game.start(Interaction)
                except AttributeError:
                    # Add error checking for none complete games
                    await Interaction.response.send_message(
                        "Failed to start game! (game code not coded correctly)"
                    )
                    self.logger.error(
                        f"Failed to start {values[0]}! Missing start function"
                    )
                break  # Don't both looping through the other games

    @commands.hybrid_command()
    async def playgame(self, ctx: commands.Context):
        """Select a game to play"""
        gameOptions = []

        # Load games into the dropdown.
        for game in self.games:
            desc: str = game.__doc__ or "No description provided"
            emoji = getattr(game, "display_emoji", "")

            gameOptions.append(
                discord.SelectOption(
                    label=type(game).__name__, description=desc, emoji=emoji
                )
            )

        view = uis.DropdownView(
            callback=self.game_select,
            placeholder="Select game to play",
            options=gameOptions,
        )
        self.msg = await ctx.send("Pick a game to play!", view=view)

    @commands.hybrid_command()
    @commands.is_owner()
    async def reloadgames(self, ctx: commands.Context):
        # Seperate reload command as it reloads different modules than the bot would reload
        """
        OWNER ONLY: Reload the currently loaded games
        """
        self.games.clear()
        for game in self.game_module:
            game = importlib.reload(game)
            self.games.append(game.game_setup(self.bot))
            self.logger.info(f"Reloaded {game} into game_loader")


async def setup(bot):
    await bot.add_cog(game_loader(bot))
