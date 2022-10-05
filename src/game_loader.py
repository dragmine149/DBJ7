import importlib
import logging
import os
import traceback
import typing

import discord
from discord.ext import commands

from .utils import bank, uis

# from .utils.paginator import Pages


class game_loader(commands.Cog, name="Games"):  # type: ignore
    """
    Play any game!
    """

    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.game_module: typing.List = []
        self.games: typing.List = []
        self.logger = logging.getLogger("bot.game")
        self.logger.info("initialized")
        self.chosenGame: str = ""

        for game in os.listdir("src/games"):
            if game.endswith(".py"):
                # Load all games, we do this to keep the game cogs seperate from the main discord bot.
                # Just makes everything better IMO.
                # Also means, we should be able to create new files without having to reload the bot

                module = importlib.import_module(f"src.games.{game[:-3]}")
                self.load_modules(module, game)

    def load_modules(self, module, name):
        self.game_module.append(module)
        self.games.append(module.game_setup(self.bot))
        self.logger.info(f"Loaded {name} into game_loader")

    @property
    def display_emoji(self) -> typing.Union[str, bytes, discord.PartialEmoji]:
        return "🎮"

    async def game_select(self, Interaction: discord.Interaction, values: list[str]):
        for game in self.games:
            if type(game).__name__ == self.chosenGame:
                try:
                    # await self.msg.delete()  # Don't know whever to delete original message or not
                    await game.start(Interaction)
                except AttributeError as e:
                    # Add error checking for none complete games
                    cnt = "ERROR: Failed to start game! (game code not coded correctly)"

                    await Interaction.followup.send(content=cnt)
                    self.logger.error(f"Failed to start {self.chosenGame}!")
                    self.logger.info(e)
                    self.logger.info(traceback.format_exc())
                break  # Don't both looping through the other games

    async def game_preLoad(self, Interaction: discord.Interaction, data: list[str]):
        self.chosenGame = data[0]  # type: ignore

        button = uis.Button(
            label="Play game!",
            callback=self.game_select,
            style=discord.ButtonStyle.primary,
            emoji="▶️",
        )

        view = discord.ui.View()
        view.add_item(button)

        await Interaction.response.send_message(
            "Press the button once you are ready!", view=view
        )

    @commands.hybrid_command()
    async def playgame(self, ctx: commands.Context, game: typing.Optional[str]):
        """
        Choose a game to gamble coins on!

        Args:
            game (option, str): Tries and loads you straight into that game
        """
        self.account = await bank.Player_Status.get_by_id(ctx.author.id)

        """Select a game to play"""
        if self.account.unlucky == 1:
            await ctx.send(
                "Oh oh! Seems likes you can't win any games. Come back in a while, you might be more lucky then."
            )
            return

        gameOptions = []

        if game is not None and game != "":
            found = False
            for possibleGames in self.games:
                if type(possibleGames).__name__ == game:
                    self.chosenGame = game  # type: ignore
                    found = True
                    await self.game_preLoad(ctx.interaction, [str(game)])
                    return

            if not found:
                await ctx.send("Game not found in currently loaded games...")

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
            callback=self.game_preLoad,
            placeholder="Select game to play",
            options=gameOptions,
        )
        self.msg = await ctx.send("Pick a game to play!", view=view)

    def reload_games(self):
        gameNames = []

        # Reload all modules first
        self.games.clear()  # remove old modules
        for game in self.game_module:  # loop through all modules
            gName = game.__name__.split(".")[2:][0]

            try:
                game = importlib.reload(game)  # reload
                self.games.append(game.game_setup(self.bot))  # add

                gameNames.append(gName)

                self.logger.info(f"Reloaded {gName} into game_loader")  # log

            # Check for module removed
            except ModuleNotFoundError:
                self.logger.warning(f"Module {game} no longer found in folder!")
                position = self.game_module.index(game)
                moduleInfo = self.games.pop(position)
                self.game_module.remove(game)
                self.logger.info(f"Removed: {moduleInfo} from game_loader")
                # TODO: remove from self.games

        # Adds new modules if they aren't already loaded
        for game in os.listdir("src/games"):
            if game.endswith(".py"):
                if game[:-3] not in gameNames:
                    module = importlib.import_module(f"src.games.{game[:-3]}")
                    self.game_module.append(module)
                    self.games.append(module.game_setup(self.bot))

                    self.logger.info(f"Added {game} into game_loader on the fly!")

    ## TODO: Find a way to have an alaises so we can run {prefix}rg instead
    @commands.hybrid_command(hidden=True)
    @commands.is_owner()
    async def reloadgames(self, ctx: commands.Context):
        # Seperate reload command as it reloads different modules than the bot would reload
        """
        OWNER ONLY: Reload the currently loaded games
        """
        self.reload_games()
        await ctx.reply("Reloaded games", ephemeral=True)


async def setup(bot):
    await bot.add_cog(game_loader(bot))
