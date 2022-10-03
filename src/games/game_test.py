from discord.ext import commands


class gameTest:
    """
    Overall view and testing for some things
    """

    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    @property
    def display_emoji(self) -> str:
        return "🧪"


def game_setup(bot):
    return gameTest(bot)
