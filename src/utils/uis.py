import typing

import discord
from discord import ui


class Multiple_Items(ui.View):
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
    def __init__(self, label: str, **kwargs):
        super().__init__(label=label, **kwargs)
        self.label_ = label
        self.value = None

    async def callback(self, interaction: discord.Interaction):
        self.value = True
