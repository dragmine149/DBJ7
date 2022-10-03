try:
    import orjson # speed
except ImportError:
    import json
import os


class FileHandler:
    def __init__(self) -> None:
        pass

    def SaveFile(self, name, data, useJson=False):
        """Saves a file

        Args:
            name (string): Name of the file to save
            data (_type_): Data to save in the file
            useJson (bool, optional): To save in a json format or not. Defaults to False.
        """
        with open(f"Data/{name}") as f:
            if not useJson:
                f.write(data)
            else:
                f.write(json.dumps(data))

    def ReadFile(self, name, useJson=False):
        """Read data from a file

        Args:
            name (string): Name of the file to read from
            useJson (bool, optional): To read the json format or not. Defaults to False.

        Returns:
            _type_: The data stored in the file
        """
        with open(f"Data/{name}") as f:
            if not useJson:
                return f.read()
            return json.loads(f.read())

    def MakeFolder(self, name):
        """Makes a folder

        Args:
            name (string): Name of the folder
        """
        try:
            os.mkdir(f"Data/{name}")
        except FileExistsError:
            pass
