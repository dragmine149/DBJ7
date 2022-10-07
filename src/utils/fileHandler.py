import orjson as json

import os

import aiofiles
import discord



class FileHandler:
    def __init__(self) -> None:
        pass

    async def SaveFile(self, name: str, data) -> None:
        """Saves a file

        Args:
            name (string): Name of folder + Discord UserID
            data (dict): Data to save in the file
        """
        parents = os.path.split(name)[0]
        if not os.path.exists("Data/" + parents):
            os.mkdir("Data/" + parents)
        if isinstance(data["user"], (discord.User, discord.Member, discord.Object)):
            data["user"] = data["user"].id
        async with aiofiles.open(f"Data/{name}", "wb") as f:
            data = json.dumps(data)  # type: ignore
            if isinstance(data, str):
                data = data.encode()  # orjson
            await f.write(data)

    async def ReadFile(self, name: str) -> dict:
        """Read data from a file

        Args:
            name (string): Name of folder + Discord UserID

        Returns:
            dict: The data stored in the file
        """
        if not os.path.exists("Data/" + name):
            raise FileNotFoundError(
                "User has no data yet (change this error: `src/utils/fileHandler: 39`)"
            )
        async with aiofiles.open(f"Data/{name}", "rb") as f:  # orjson moment
            return json.loads(await f.read())  # type: ignore


if not os.path.exists("Data"):
    os.mkdir("Data")
