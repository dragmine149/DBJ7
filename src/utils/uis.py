import logging
import typing

import discord
from discord import ui

logger = logging.getLogger("bot.ui.log")
logger.info("initialized")


class Button(ui.Button):
    """
    A class to show a button on an object
    """

    def __init__(
        self,
        label: typing.Optional[str],
        callback=None,
        **kwargs,
    ):
        """
        Args:
            label (typing.Optional[str]): The text to show on the button
            callback (_type_, optional): What function to call once button press. Defaults to None. Required Inputs (Interaction: discord.Interaction, label: str).
            style (ButtonStyle, optional): The style of the button_. Defaults to ButtonStyle.secondary.
            disabled (bool, optional): Can the button be clicked?. Defaults to False.
            url (typing.Optional[str], optional): URL to open on button click. Defaults to None.
            emoji (typing.Optional[typing.Union[str, Emoji, PartialEmoji]], optional): Emoji to show on the button. Defaults to None.
            row (typing.Optional[int], optional): What row to put the button on. Defaults to None (automatic).
        """
        super().__init__(label=label, **kwargs)

        self.callbackFunc = callback
        if self.callbackFunc is None:
            self.callbackFunc = self.defaultCallBack
        self.clicked: bool = False

    async def callback(self, Interaction: discord.Interaction):
        await self.callbackFunc(Interaction, self.label)
        self.clicked = True

    async def defaultCallBack(self, Interaction: discord.Interaction, label: str):
        await Interaction.response.send_message(f"You clicked: {label}")
        logger.warning("Default callback used for button class!")


class Multiple_Buttons(ui.View):
    """
    Shows multiple buttons on the message
    """

    def __init__(self, data=[]):
        super().__init__(timeout=60)

        for buttonData in data:
            self.Add_Button(**buttonData)

    components: typing.List[Button] = []

    def Add_Button(self, label: typing.Optional[str], callback=None, **kwargs) -> None:
        """
        Args:
            label (typing.Optional[str]): The text to show on the button
            callback (_type_, optional): What function to call once button press. Defaults to None. Required Inputs (Interaction: discord.Interaction, label: str).
            style (ButtonStyle, optional): The style of the button_. Defaults to ButtonStyle.secondary.
            disabled (bool, optional): Can the button be clicked?. Defaults to False.
            url (typing.Optional[str], optional): URL to open on button click. Defaults to None.
            emoji (typing.Optional[typing.Union[str, Emoji, PartialEmoji]], optional): Emoji to show on the button. Defaults to None.
            row (typing.Optional[int], optional): What row to put the button on. Defaults to None (automatic).
        """
        obj = Button(label, callback, **kwargs)

        self.add_item(obj)
        self.components.append(obj)

    @property
    def choosen(self) -> "Button":
        return [button for button in self.components if button.clicked][0]

    def Edit_Button(self, index, **kwargs):
        # TODO: make it so we can edit a button on the go, instead of recreating a button.
        pass


# Pretty much taken from the exmaples: https://github.com/Rapptz/discord.py/blob/master/examples/views/dropdown.py just modified
class Dropdown(ui.Select):
    """
    Shows a dropdown menu of items
    """

    def __init__(self, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.callbackFunc = callback
        if self.callbackFunc is None:
            self.callbackFunc = self.defaultCallback

    async def callback(self, interaction: discord.Interaction):
        await self.callbackFunc(
            interaction, self.values
        )  # calls the callback function so the data result can be processed somewhere else

    async def defaultCallback(
        self, interaction: discord.Interaction, values: list[str]
    ):
        # The default callback function if nothing selected
        await interaction.response.send_message(f"You choice: {values[0]}")
        logger.warn("Default callback used! Please assign a callback!")


class DropdownView(ui.View):
    """
    Main dropdown view class
    """

    def __init__(self, callback=None, **kwargs):
        """
        Args:
            callback (function, optional): The function to call (just have the name, not the actuall call) when something happense. Requires discord.Interaction input
            placeholder (str, optional): Value to show in the dropdown ui. Defaults to "".
            min_values (int, optional): Minium amount of items the user can select. Defaults to 1.
            max_values (int, optional): Maxium amount of items the user can select. Defaults to 1.
            options (list, optional): The options to show in the ui. Defaults to [].
        """
        super().__init__(timeout=60)
        self.add_dropdown(callback, **kwargs)

    def add_dropdown(self, callback=None, **kwargs):
        """If you want to add a new dropdown menu in the ui you can. Just not recommened."""
        self.add_item(Dropdown(callback, **kwargs))
