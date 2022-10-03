import typing
import logging
import discord
from discord import ui

logger = logging.getLogger('bot.log')
logger.info('initialized')

class Multiple_Items(ui.View):
    """
    Lets you show multiple buttons on the ui
    """

    def __init__(self, items: typing.List):
        super().__init__(timeout=10)
        self.options = [Button(item) for item in items]
        for item in self.options:
            self.add_item(item)

    def check(self):
        for option in self.options:
            if option.value == True:
                return option.label_


class Button(ui.Button):
    """
    Lets you show a button on the ui
    """

    def __init__(self, label: str, **kwargs):
        super().__init__(label=label, **kwargs)
        self.label_ = label
        self.value: typing.Optional[bool] = None

    async def callback(self, interaction: discord.Interaction):
        self.value = True


# Pretty much taken from the exmaples: https://github.com/Rapptz/discord.py/blob/master/examples/views/dropdown.py just modified
class Dropdown(ui.Select):
    """
    Shows a dropdown menu of items
    """

    def __init__(
        self,
        callback=None,
        placeholder: str = "",
        min_values: int = 1,
        max_values: int = 1,
        options: list = [],
    ):
        super().__init__(
            placeholder=placeholder,
            min_values=min_values,
            max_values=max_values,
            options=options,
        )
        self.callbackFunc = callback
        if self.callbackFunc is None:
            self.callbackFunc = self.defaultCallback

    async def callback(self, interaction: discord.Interaction):
        await self.callbackFunc(
            interaction,
            self.values
        )  # calls the callback function so the data result can be processed somewhere else

    async def defaultCallback(self, interaction: discord.Interaction, values: list[str]):
        # The default callback function if nothing selected
        await interaction.response.send_message(f"You choice: {values[0]}")
        logger.warn("Default callback used! Please assign a callback!")
        


class DropdownView(ui.View):
    """
    Main dropdown view class
    """

    def __init__(
        self,
        callback=None,
        placeholder: str = "",
        min_values: int = 1,
        max_values: int = 1,
        options: list = [],
    ):
        """
        Args:
            callback (function, optional): The function to call (just have the name, not the actuall call) when something happense. Requires discord.Interaction input
            placeholder (str, optional): Value to show in the dropdown ui. Defaults to "".
            min_values (int, optional): Minium amount of items the user can select. Defaults to 1.
            max_values (int, optional): Maxium amount of items the user can select. Defaults to 1.
            options (list, optional): The options to show in the ui. Defaults to [].
        """
        super().__init__()

        self.add_item(Dropdown(callback, placeholder, min_values, max_values, options))
