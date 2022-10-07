from ..utils import game_template,bank,MoneySelector,uis
from discord.ext import commands
import dataclasses
import aiofiles
import os
import random
import typing
import discord

@dataclasses.dataclass
class Dictionary:
    prompt: str
    possible_words: list[str]
    
    @property
    def get_possibles_words(self) -> int:
        return len(self.possible_words)
    
    @classmethod
    async def create(cls, prompt_length:int) -> None:
        async with aiofiles.open(os.path.join(os.path.realpath(__file__), "words.txt"), "r") as f:
            words = [x for x in (await f.read()).splitlines()]
        selected = random.choice(words)
        prompt = ""
        if len(prompt) <= prompt_length:
            return await cls.create(prompt_length)
        while len(prompt) != prompt_length:
            prompt += random.choice(selected)
        possible_words = [x for x in words if prompt in x]
        if (len(possible_words) <= 100 and not prompt_length >= 4):
            return await cls.create(prompt_length)
        return cls(prompt, possible_words)
class Bomb_Party(game_template.Template):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        bank.bot = bot
        self.betting_value = 0
        self.dictionary: typing.Optional[Dictionary] = None
        self.interaction: discord.Interaction = None
        self.account: bank.Player_Status = None
        self.multiplier = 1
    async def money_callback(self, value: int) -> None:
        self.betting_value = value
        await self.difficulty_selector()
        
    async def easy(self,interaction: discord.Interaction, value: str):
        self.multiplier = 1
        self.dictionary = await Dictionary.create(random.randint(1,2))
        
    async def normal(self, interaction: discord.Interaction, value: str):
        self.multiplier = 1.5
        self.dictionary = await Dictionary.create(random.randint(1,3))
    async def hard(self, interaction: discord.Interaction, value: str):
        self.multiplier = 2
        self.dictionary = await Dictionary.create(random.randint(2,4))
        
    async def impossible(self, interaction: discord.Interaction, value: str):
        self.multiplier = 4
        self.dictionary = await Dictionary.create(random.randint(3,5))
    async def difficulty_selector(self):
        ui = uis.Multiple_Buttons()
        ui.Add_Button(
            "Easy (2 Prompts 1x multiplier)",
            self.easy
        )
        ui.Add_Button(
            "Normal ("
        )
        
    async def start(self, interaction: discord.Interaction) -> None:
        await MoneySelector.MoneySelector(interaction,self.money_callback).get_money()
        self.interaction = interaction
def game_setup(bot: commands.Bot) -> Bomb_Party:
    return Bomb_Party(bot)