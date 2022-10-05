import asyncio
import random

import discord
from discord.ext import commands

from ..utils import MoneySelector, bank, game_template, uis


class GuessNumber(game_template.Template):
    """
    Guess number with difficulties
    There's 4 difficulties with different multiplier
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bank.bot = bot
        self.bet: int = None
        self.interaction: discord.Interaction = None
        self.account: bank.Player_Status = None
        self.confirmed = False

    async def callback_money(self, value: int):
        self.bet = value
        await self.actually_starting_the_game_with_rapid_pace_on_god()

    async def easy(self, interaction: discord.Interaction, label: str):
        await self.start_game(10, interaction)

    async def medium(self, interaction: discord.Interaction, label: str):
        await self.start_game(25, interaction)

    async def hard(self, interaction: discord.Interaction, label: str):
        await self.start_game(50, interaction)

    async def impossible(self, interaction: discord.Interaction, label: str):
        await self.start_game(200, interaction)

    async def confirmation_yes(self, interaction: discord.Interaction, label: str):
        self.confirmed = True

    async def confirmation_no(self, interaction: discord.Interaction, label: str):
        self.confirmed = False

    async def start_game(self, range: int, interaction: discord.Interaction):
        mapped = {10: 0.5, 25: 0.85, 50: 1, 200: 2}
        self.interaction = interaction
        number = random.randint(1, range)
        self.guesses = 0
        self.account = await bank.Player_Status.get_by_id(self.interaction.user.id)
        if self.bet > self.account.money:
            await self.interaction.response.send_message(
                "You don't have enough money to bet that much!", ephemeral=True
            )
            return

        await self.interaction.edit_original_response(
            content=f"Guess a number between 1 and {range}"
        )
        modal = uis.AskNumber_Modal(title="Provide answer here")
        await self.interaction.response.send_modal(modal=modal)
        await modal.wait()
        if modal.answer is None:
            return await self.interaction.followup.send(
                "You didn't provide an answer", ephemeral=True
            )
        confirmation = uis.Multiple_Buttons()
        confirmation.Add_Button(
            "Yes", self.confirmation_yes, style=discord.ButtonStyle.primary
        )
        confirmation.Add_Button(
            "No", self.confirmation_no, style=discord.ButtonStyle.danger
        )
        await self.interaction.response.send_message(
            f"Are you sure you want to guess {modal.answer}?", view=confirmation
        )
        await confirmation.wait()
        await asyncio.sleep(1)
        if not self.confirmed:
            return await self.interaction.edit_original_response(content="Cancelled")
        answer = modal.answer.value
        if number == answer:
            await self.interaction.edit_original_message(
                content=f"You won! You got the number right!\nPrize: {self.bet * mapped[range]}"
            )
            self.account.money += self.bet * mapped[range]
        elif number > answer:
            await self.interaction.edit_original_message(
                content=f"Your answer was too low\nThe number was {number}\nPrize: -{self.bet * mapped[range]}"
            )
            self.account.money -= self.bet * mapped[range]
        elif number < answer:
            await self.interaction.edit_original_message(
                content=f"Your answer was too high\nThe number was {number}\nPrize: -{self.bet * mapped[range]}"
            )
            self.account.money -= self.bet * mapped[range]

    async def actually_starting_the_game_with_rapid_pace_on_god(self):
        ui = uis.Multiple_Buttons()
        ui.Add_Button(
            "Easy (10 range, 0.5 multiplier)",
            self.easy,
            style=discord.ButtonStyle.primary,
        )
        ui.Add_Button(
            "Medium (25 range, 0.85 multiplier)",
            self.medium,
            style=discord.ButtonStyle.primary,
        )
        ui.Add_Button(
            "Hard (50 range, 1 multiplier)",
            self.hard,
            style=discord.ButtonStyle.primary,
        )
        ui.Add_Button(
            "Impossible 💀 (200 range, 2 multiplier)",
            self.impossible,
            style=discord.ButtonStyle.primary,
        )
        await self.interaction.edit_original_response(
            content="Please select a difficulty", view=ui
        )
        await ui.wait()

    async def start(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.interaction = interaction
        self.account = await bank.Player_Status.get_by_id(self.interaction.user.id)
        await MoneySelector.MoneySelector(
            self.interaction, self.callback_money
        ).get_money()

    @property
    def display_emoji(self):
        return "🔢"


def game_setup(bot: commands.Bot):
    return GuessNumber(bot)
