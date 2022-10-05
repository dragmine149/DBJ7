from discord.ext import commands


class gameTest:
    """
    Run some tests for some functionalities.
    """

    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> str:
        return "🧪"


def game_setup(bot):
    return gameTest(bot)
