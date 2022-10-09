import importlib
import logging
import os
import traceback
import typing
from datetime import datetime

import discord
from discord.ext import commands
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver

from .utils import bank, uis  # type: ignore

"""
game_loader
- A loader designed to keep games seperate from the main bot
- Cogs in cogs, basically.

Benefits:
- Help command doesn't include games, we can have seperate help command for that.
- Reloading doesn't reload all the cogs, instead only the games
"""


class game_loader(commands.Cog, name="Games"):  # type: ignore
    """
    Play any game!
    """

    @property
    def display_emoji(self) -> typing.Union[str, bytes, discord.PartialEmoji]:
        return "🎮"

    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.game_module: typing.List = []
        self.games: typing.List = []
        self.module_names: typing.List = []

        # logger inforamtion
        self.logger = logging.getLogger("bot.game")
        self.logger.info("initialized")

        self.chosenGame: str = ""
        self.msg: discord.Interaction | None = None
        bank.bot = bot

        observer = PollingObserver()

        def on_modified(event):
            if (
                not event.is_directory
            ):  # checks for file modified instead of file creation
                self.logger.info(f"Game source code changed: {event.src_path}")
                if event.src_path.endswith(".py") and not event.src_path.startswith(
                    "_"
                ):
                    self.reload_game(os.path.split(event.src_path)[1][:-3])
                    self.logger.info("Reloaded game loader")

        eH = FileSystemEventHandler()
        eH.on_modified = on_modified
        observer.schedule(eH, "src/games", recursive=False)
        observer.start()

        # Startup loding of games
        self.reload_games()

    async def game_select(self, Interaction: discord.Interaction):
        for game in self.games:
            if (
                type(game).__name__ == self.chosenGame
                or self.chosenGame in game.aliases
                or self.chosenGame == getattr(game, "modName", None)
            ):
                try:
                    await game.start(Interaction)
                except AttributeError as e:
                    # Add error checking for none complete games
                    await Interaction.followup.send(
                        content="ERROR: Failed to start game! (game code not coded correctly)"
                    )
                    self.logger.error(f"Failed to start {self.chosenGame}!")
                    self.logger.info(e)
                    self.logger.info(traceback.format_exc())

                return  # stops the loop and the function

    async def game_cancel(self, Interaction: discord.Interaction):
        await Interaction.response.send_message("Canceled playing...", ephemeral=True)

    async def game_premethod(self, Interaction: discord.Interaction, label: str):
        await self.confirmInteract.delete()  # delete old stuff

        if label == "Play game!":
            return await self.game_select(Interaction)
        if label == "Cancel":
            return await self.game_cancel(Interaction)

    async def game_preLoad(self, Interaction: discord.Interaction, data: list[str]):
        self.chosenGame = data[0]  # type: ignore
        if self.msg is not None:
            await self.msg.delete()  # delete dropdown message
            self.msg = None

        view = uis.Multiple_Buttons(
            [
                {
                    "label": "Play game!",
                    "callback": self.game_premethod,
                    "style": discord.ButtonStyle.primary,
                    "emoji": "▶️",
                },
                {
                    "label": "Cancel",
                    "callback": self.game_premethod,
                    "style": discord.ButtonStyle.danger,
                    "emoji": "❎",
                },
            ]
        )

        # Checks the message and makes sure we have a message
        msg = None
        if Interaction.message is None:
            raise ValueError("Interaction.message is None")

        if type(Interaction.channel) is not discord.TextChannel:
            raise ValueError("Command called not in a text channel!")

        msg = await Interaction.channel.send(f"Play {self.chosenGame}?", view=view)

        self.confirmInteract = msg

    async def process_gameInput(
        self, ctx: commands.Context, game: typing.Optional[str]
    ) -> bool:

        if ctx.author.id != self.pguser.id:
            return await ctx.send("You can not use this interaction!", ephemeral=True)

        for possibleGames in self.games:

            orGameName = type(possibleGames).__name__
            gameName = ""
            try:
                gameName = possibleGames.name
            except AttributeError:
                self.logger.warning(f"{gameName} has no attribute `name`")
                gameName = orGameName

            if gameName == game:
                self.chosenGame = game  # type: ignore
                await self.game_preLoad(ctx, [orGameName])
                return True

            # Suport for game name aliases
            try:
                aliases = possibleGames.aliases
                if game in aliases:
                    self.chosenGame = game  # type: ignore
                    await self.game_preLoad(ctx, [orGameName])
                    return True

            except AttributeError:
                self.logger.warning(
                    f"{orGameName} has no attribute `aliases` please refer to src.games.README.md for more information"
                )

        await ctx.send("Game not found in currently loaded games...")
        return False

    @commands.hybrid_command(aliases=["play"])
    async def playgame(self, ctx: commands.Context, game: typing.Optional[str]):
        """
        Choose a game to gamble coins on!
        Args:
            game (option, str): Tries and loads you straight into that game
        """
        self.account = await bank.Player_Status.get_by_id(ctx.author.id)
        self.pguser = ctx.author

        # Check for account paid debt
        if (
            self.account.last_paid_debt
            and (datetime.now() - self.account.last_paid_debt).days > 7
        ):
            return await ctx.reply(
                "You're prohibited to play any games since you have debts and you didn't paid any for a week straight. Go pay your debt to play the game!"
            )
        # Check for unlucky being 1 (impossible)
        if self.account.unlucky == 1:
            return await ctx.reply(
                "Oh oh! Seems likes you can't win any games. Come back in a while, you might be more lucky then."
            )

        # Process the inputted game
        if game is not None and game != "":
            result = await self.process_gameInput(ctx, game)
            # Return if succesffully found game
            if result:
                return

        gameOptions = []
        # Load games into the dropdown.
        for gameInfo in self.games:
            if gameInfo is None:
                self.logger.error(f"Found None as a game in self.games")
                continue

            desc: str = gameInfo.__doc__ or "No description provided"
            emoji = getattr(gameInfo, "display_emoji", "❔")

            gameName: str = type(gameInfo).__name__
            try:
                gameName = gameInfo.modName
            except AttributeError:
                self.logger.warning(f"{gameName} has no attribute `modName`")

            gameOptions.append(
                discord.SelectOption(label=gameName, description=desc, emoji=emoji)
            )
        view = uis.DropdownView(
            callback=self.game_preLoad,
            owner=ctx.author
            placeholder="Select game to play",
            options=gameOptions,
        )
        try:
            self.msg = await ctx.send("Pick a game to play!", view=view)
        except discord.errors.HTTPException as HTTP:
            self.logger.error("Http error whilst trying to send message")
            self.logger.debug(HTTP)
            self.logger.debug(traceback.format_exc())

            self.logger.info("-----------")
            for option in gameOptions:
                self.logger.debug(option)
            self.logger.info("-----------")

    # reloads one game in particalar
    def reload_game(self, module: str) -> str:
        """
        Reloads a specific module.
        If module not loaded, will load
        If module got deleted, will remove

        Args:
            module (str): The name of the module (without the .py)

        Returns:
            str: What happened on reloading
        """
        # Check if module already loaded
        if module not in self.module_names:
            self.logger.info(f"Adding {module} to game_loader")

            # Import module into script
            moduleInfo = importlib.import_module(f"src.games.{module}")
            classInfo = None

            try:
                classInfo = moduleInfo.game_setup(self.bot)
            except AttributeError:
                self.logger.error(
                    f"File src.games.{module} failed to load! Either because of below error or missing function `game_setup`"
                )
                self.logger.error(traceback.format_exc())
                return "Failed import"
            except Exception:  # Anything else
                self.logger.error(
                    f"File src.games.{module} failed to load! Skipping! (Please see the error log below)"
                )
                self.logger.error(traceback.format_exc())
                return "Failed import"

            self.game_module.append(moduleInfo)
            self.games.append(classInfo)
            self.module_names.append(module)
            return "Added module"

        position = self.module_names.index(module)

        # Check if module still exists
        if f"{module}.py" not in os.listdir("src/games"):
            self.logger.warning(f"{module} no longer found in src.games")

            # Remove data
            moduleInfo = self.games.pop(position)
            del self.game_module[position]
            self.module_names.remove(module)

            self.cog_load.info(f"Removed {moduleInfo} from game_loader")
            return "Removed module"

        # If module exists, hasn't been created, then we reload
        self.logger.info(f"Reloading {module} in game_loader")
        gameInfo = self.game_module[position]
        gameInfo = importlib.reload(gameInfo)

        try:
            self.games[position] = gameInfo.game_setup(self.bot)
            return "Reloaded module"
        except AttributeError:
            self.logger.error(
                f"File src.games.{module} does not contain a function called 'game_setup'! Please check the spelling of the function"
            )
            return "Failed reload"
        except RuntimeError:
            self.logger.error("File observer might have stopped for `src.games`")

        return "Error return! (Something failed badly)"

    # Reload all game modules
    def reload_games(self, module=None) -> str:
        self.logger.info("---------------------")
        if module is not None:
            return self.reload_game(module)

        # Reload all modules first
        for game in os.listdir("src/games"):  # loop through all modules
            if game.endswith(".py"):
                if game != "__init__.py":
                    log = self.reload_game(game[:-3])
                    self.logger.info(f"{game[:-3]}: {log}")

        self.logger.info("---------------------")
        return "Reloded all games"

    ## TODO: Find a way to have an alaises so we can run {prefix}rg instead
    @commands.hybrid_command(hidden=True, aliases=["rg"])
    @commands.is_owner()
    async def reloadgames(
        self, ctx: commands.Context, module: typing.Optional[str] = None
    ):
        # Seperate reload command as it reloads different modules than the bot would reload
        """
        OWNER ONLY: Reload the currently loaded games

        Args:
            module (str, optional): The file name of the module to reload. Will only reload this module. Defaults: None.
        """
        await ctx.defer()
        await ctx.reply(self.reload_games(module), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(game_loader(bot))
