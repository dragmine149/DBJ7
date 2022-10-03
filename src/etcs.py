import platform
import sys
from datetime import datetime

import discord
import psutil
from discord.ext import commands

from .utils import time

sys.path.append("..")
import config


class Stuff(
    commands.Cog,
):
    """
    Miscellaneous commands and stuffs that don't fit anywhere else.
    """

    def __init__(self, bot):
        self.bot = bot

    @property
    def display_emoji(self):
        return "💭"

    async def cog_before_invoke(self, ctx: commands.Context):
        await ctx.defer()

    @commands.hybrid_command(name="credits", aliases=["c"])
    async def credits(self, ctx: commands.Context):
        """
        Shows the credits.
        """
        embed = discord.Embed(
            title="Credits", description="Thanks to everyone who using this bot!"
        )

        embed.add_field(name="Creator", value="[Unpredictable#9443] ")
        embed.add_field(
            name="The bot is also open-source!",
            value=config.git_repo,
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="ping", aliases=["p"])
    async def ping(self, ctx: commands.Context):
        """
        Pong!
        """
        embed = discord.Embed(
            title="Pong!",
            description=f"{round(self.bot.latency * 1000)} ms from API websocket",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="status")
    async def status(self, ctx: commands.Context):
        """
        Status of bot like uptime, memory usage, etc.
        """
        embed = discord.Embed(
            title="Status", description="Bot status", color=discord.Color.green()
        )
        embed.add_field(name="CPU", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="RAM", value=f"{psutil.virtual_memory().percent}%")
        embed.add_field(name="Disk", value=f"{psutil.disk_usage('/').percent}%")
        embed.add_field(
            name="Uptime",
            value=f"{time.human_timedelta(datetime.utcnow(), source=self.bot.start_time)}",
        )
        embed.add_field(name="Python", value=f"{platform.python_version()}")
        embed.add_field(name="Discord.py", value=f"{discord.__version__}")
        embed.add_field(name="Bot version", value=f"{self.bot.version_}")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="invite", aliases=["i"])
    async def invite(self, ctx: commands.Context):
        """
        Invite the bot to your server.
        """
        embed = discord.Embed(
            title="Invite",
            description="Invite the bot to your server!",
            color=discord.Color.green(),
        )
        embed.add_field(
            name="Invite link",
            value=f"[Click here](https://discord.com/api/oauth2/authorize?client_id{self.bot.user.id}=&permissions=8&scope=bot%20applications.commands)",
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="raise")
    @commands.is_owner()
    async def raise_error(self, ctx: commands.Context):
        """
        Raise an error.
        """
        raise RuntimeError("This is a test error.")


async def setup(bot):
    await bot.add_cog(Stuff(bot))
