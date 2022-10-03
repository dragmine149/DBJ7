try:
    import orjson # speed
except ImportError:
    import json
import os

import aiofiles

class FileHandler:
    def __init__(self) -> None:
        pass

    async def SaveFile(self, userID:int, data: dict) -> None:
        """Saves a file

        Args:
            userID (string): discord userID to save data for
            data (_type_): Data to save in the file
        """
        async with aiofiles.open(f"Data/{userID}.json") as f:
            await f.write(json.dumps(data))

    async def ReadFile(self, userID: int) -> dict:
        """Read data from a file

        Args:
            userID (string): discord userID to read data for

        Returns:
            _type_: The data stored in the file
        """
        async with aiofiles.open(f"Data/{userID}.json") as f:
            return await json.loads(f.read())


if not os.path.exists("Data"):
    os.mkdir("Data")
