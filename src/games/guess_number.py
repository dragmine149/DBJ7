import asyncio
import random

import discord
from discord.ext import commands

from src.utils import MoneySelector, bank, game_template, uis


class GuessNumber(game_template.Template):
    """
    Guess number with difficulties
    There's 4 difficulties with different multiplier
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bank.bot = bot
        self.bet: int = 0
        self.interaction: discord.Interaction = None  # type: ignore
        self.account: bank.Player_Status = None  # type: ignore
        self.confirmed = False

    async def callback_money(self, value: int, user):
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
        await interaction.response.defer()
        self.confirmed = True
        if self.number == self.answer:
            await self.interaction.edit_original_response(
                content=f"You won! You got the number right!\nPrize: {self.bet +(self.bet * self.mapped[self.range])}"
            )
            try:
                if "coin_multiplier" in [
                    x.effect_name
                    for x in self.account.effects
                    if x.effect_name == "coin_multiplier"
                ] and (
                    not [
                        x
                        for x in self.account.effects
                        if x.effect_name == "coin_multiplier"
                    ][0].game_name
                    or [
                        x
                        for x in self.account.effects
                        if x.effect_name == "coin_multiplier"
                    ][0].game_name.lower()
                    == "guess_number"
                ):
                    selected = None
                    for effect in self.account.effects:
                        if effect.effect_name == "coin_multiplier":
                            selected = effect
                            break
                    self.account.money += (
                        self.bet
                        + (self.bet * self.mapped[self.range])
                        + (self.bet * selected.coin_multiplier)
                    )
            except Exception:
                self.account.money += self.bet + (self.bet * self.mapped[self.range])
        elif self.number > self.answer:
            await self.interaction.edit_original_response(
                content=f"Your answer was too low\nThe number was {self.number}\nPrize: -{self.bet +(self.bet * self.mapped[self.range])}"
            )
            self.account.money -= self.bet + (
                self.bet * self.mapped[self.range]
            )  # type: ignore
        elif self.number < self.answer:
            await self.interaction.edit_original_response(
                content=f"Your answer was too high\nThe number was {self.number}\nPrize: -{self.bet +(self.bet * self.mapped[self.range])}"
            )
            self.account.money -= self.bet + (
                self.bet * self.mapped[self.range]
            )  # type: ignore

    async def confirmation_no(self, interaction: discord.Interaction, label: str):
        await interaction.response.send_message("Cancelled", ephemeral=True)
        self.confirmed = False

    async def start_game(self, range: int, interaction: discord.Interaction):
        await interaction.response.defer()
        self.mapped = {10: 0.5, 25: 0.85, 50: 1, 200: 2}
        self.interaction = interaction
        self.number = random.randint(1, range)
        self.guesses = 0
        self.account = await bank.Player_Status.get_by_id(self.interaction.user.id)
        if self.bet > self.account.money:
            await self.interaction.edit_original_response(
                content="You don't have enough money to bet that much!"
            )
            return

        await self.interaction.edit_original_response(
            content=f"Guess a number between 0 and {range} by type it in chat!",
            view=None,
        )
        try:
            self.answer = int(
                (
                    await self.bot.wait_for(
                        "message",
                        check=lambda m: m.author == self.interaction.user
                        and m.channel == self.interaction.channel,
                    )
                ).content
            )
            assert self.answer > 0
        except asyncio.TimeoutError:
            return await self.interaction.response.send_message(
                "You took too long to answer", ephemeral=True
            )
        except ValueError:
            return await self.interaction.response.send_message(
                "You didn't enter a number", ephemeral=True
            )
        except AssertionError:
            return await self.interaction.response.send_message(
                "Number lower than 0 isn't allowed"
            )
        confirmation = uis.Multiple_Buttons()
        confirmation.Add_Button(
            "Yes", self.confirmation_yes, style=discord.ButtonStyle.primary
        )
        confirmation.Add_Button(
            "No", self.confirmation_no, style=discord.ButtonStyle.danger
        )
        self.range = range
        await self.interaction.edit_original_response(
            content=f"Are you sure you want to guess {self.answer}?", view=confirmation
        )
        await confirmation.wait()

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
