import discord
from discord.ext import commands
from dotenv import load_dotenv
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from config import config

load_dotenv()
import asyncio
import datetime
import logging
import os
import signal
import subprocess
import traceback

formatting = logging.Formatter("[%(asctime)s] - [%(levelname)s] [%(name)s] %(message)s")

logging.basicConfig(
    level=logging.NOTSET,
    format="[%(asctime)s] - [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)

log = logging.getLogger("")
log.setLevel(logging.NOTSET)

try:
    os.mkdir("logs")
except FileExistsError:
    pass
with open("logs/bot.log", "w") as f:
    f.write("")
f = logging.FileHandler("logs/bot.log", "r")
f.setFormatter(formatting)
log.addHandler(f)

logging.getLogger("discord").setLevel(logging.WARNING)  # mute

bot = commands.Bot(command_prefix=config.prefix, intents=discord.Intents.all())
bot.log = log

observer = Observer()


class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        log.info(f"File changed: {event.src_path}")
        if event.src_path.endswith(".py"):
            log.info("Reloading...")
            path = event.src_path.replace("\\", "/").replace("/", ".")[:-3]
            try:
                asyncio.run(bot.reload_extension(path))
                log.info(f"Reloaded {path}")
            except Exception as e:
                log.error(f"Failed to reload {path}")
                log.error(e)
                log.error(traceback.format_exc())


observer.schedule(FileHandler(), path="src", recursive=False)


def get_git_revision_short_hash() -> str:
    return (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .decode("ascii")
        .strip()
    )


def get_version():
    """Checks if the bot is running on the current latest version.

    Returns:
        String: Information about twhat the bot is running on
    """
    is_updated = subprocess.check_output("git status", shell=True).decode("ascii")

    if "modified" in is_updated:
        is_updated = None
    elif (
        "up to date" in is_updated
        or "nothing to commit, working tree clean" in is_updated
    ):
        is_updated = True
    else:
        is_updated = False

    if is_updated:
        return f"latest ({get_git_revision_short_hash()})"
    if is_updated is None:
        return f"latest ({get_git_revision_short_hash()}) (modified)"
    return f"old ({get_git_revision_short_hash()}) - not up to date"


@bot.event
async def on_ready():
    log.info("Logged in as")
    log.info(bot.user.name)
    log.info(bot.user.id)
    log.info("------")
    await bot.change_presence(activity=discord.Game(name=f"{config.prefix}help"))
    await bot.tree.sync()


async def main():
    try:
        started = False
        while not started:
            async with bot:
                for extension in os.listdir("src"):
                    if extension.endswith(".py") and not extension.startswith("_"):
                        await bot.load_extension(f"src.{extension[:-3]}")
                        log.info(f"Loaded extension {extension[:-3]}")
                await bot.load_extension("jishaku")
                log.info("Loaded jishaku")

                observer.start()
                signal.signal(signal.SIGINT, lambda x, y: observer.stop())
                signal.signal(signal.SIGABRT, lambda x, y: observer.stop())
                signal.signal(signal.SIGTERM, lambda x, y: observer.stop())

                log.info("Started file watcher")
                bot.start_time = datetime.datetime.utcnow()
                bot.version_ = get_version()
                log.info(
                    f"Started with version {bot.version_} and started at {bot.start_time}"
                )
                try:
                    await bot.start(config.token)
                except discord.errors.HTTPException:
                    log.exception("You likely got ratelimited or bot's token is wrong")
                started = True  # break loop
    except KeyboardInterrupt:
        log.info("Exiting...")


if __name__ == "__main__":
    asyncio.run(main())
    observer.stop()
