try:
    import orjson as json  # speed
except ImportError:
    import json  # type: ignore

import os

import aiofiles
import discord
from datetime import datetime
import typing
from .bank import Player_Status, Inventory
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

        async with aiofiles.open(f"Data/{name}", "wb") as f:
            data = json.dumps(data,default=self.serializer)  # type: ignore
            if isinstance(data, str):
                data = data.encode()  # orjson
            await f.write(data)

    def serializer(self,obj) -> typing.Any:
        if isinstance(obj, datetime):
            return obj.timestamp()
        elif isinstance(obj, (discord.User,discord.Member,discord.Object)):
            return obj.id
        elif isinstance(obj, (Player_Status, Inventory)):
            return obj.to_dict
        else:
            raise ValueError("Unable to verify")
        

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
