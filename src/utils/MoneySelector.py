import discord
from src.utils import uis


class MoneySelector:
    def __init__(self, Interaction: discord.Interaction, callback=None) -> None:
        self.Interaction = Interaction
        self.callback = callback
        if self.callback is None:
            self.callback = self.defaultCallBack
        
        self.value = 0
        
        self.view = uis.Multiple_Buttons()
        self.view.Add_Button(
            "+100",
            self.changeValue,
            style=discord.ButtonStyle.primary,
            emoji="💵"
        )
        self. view.Add_Button(
            "+10",
            self.changeValue,
            style=discord.ButtonStyle.primary,
        )
        self.view.Add_Button(
            '+1',
            self.changeValue,
            style=discord.ButtonStyle.primary
        )
        self.view.Add_Button(
            '-100',
            self.changeValue,
            style=discord.ButtonStyle.danger,
            emoji='💴',
            row=1,
        )
        self.view.Add_Button(
            '-10',
            self.changeValue,
            style=discord.ButtonStyle.danger,
            row=1,
        )
        self.view.Add_Button(
            '-1',
            self.changeValue,
            style=discord.ButtonStyle.danger,
            row=1,
        )
        self.view.Add_Button(
            'Confirm',
            self.FinishedCallback,
            style=discord.ButtonStyle.success,
            emoji='✅',
            row=2
        )
        
    async def defaultCallBack(self, value):
        await self.Interaction.edit_original_response(f"You choice {value}")
    
    async def FinishedCallback(self, Interaction: discord.Interaction, label: str):
        await self.callback(self.value)
    
    async def changeValue(self, Interaction: discord.Interaction, label: str):
        money = int(label[1:])
        if label[0] == "+":
            self.value += money
        if label[0] == "-":
            self.value -= money
            
        await Interaction.response.send_message(content=f"Changed ammount betting by: {money}", ephemeral=True)
        await self.Interaction.edit_original_response(content=f"How much money do you want to bet? Currently betting: {self.value}", view=self.view)
    
    async def show_message(self):
        await self.Interaction.edit_original_response(content=f"How much money do you want to bet? Currently betting: {self.value}", view=self.view)

    async def get_money(self):
        await self.show_message()