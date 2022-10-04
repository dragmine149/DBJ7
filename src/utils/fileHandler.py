try:
    import orjson  # speed
except ImportError:
    import json

import os

import aiofiles


class FileHandler:
    def __init__(self) -> None:
        pass

    async def SaveFile(self, name: str, data: dict) -> None:
        """Saves a file

        Args:
            name (string): Name of folder + Discord UserID
            data (dict): Data to save in the file
        """
        parents = os.path.split(name)[0]
        if not os.path.exists("Data/" + parents):
            os.mkdir("Data/" + parents)

        async with aiofiles.open(f"Data/{name}", "w") as f:
            await f.write(json.dumps(data))

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

        async with aiofiles.open(f"Data/{name}", "r") as f:
            return await json.loads(f.read())  # type: ignore


if not os.path.exists("Data"):
    os.mkdir("Data")
