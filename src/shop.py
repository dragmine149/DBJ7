import logging
import random
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks

from .utils import bank
from .utils.enums import Items


class Inventory_And_Shop(commands.Cog, name="Inventory and shop"):
    """
    Inventory and shop group commands
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_effects.start()
        self.log = logging.getLogger("bot.Inventory_And_Shop")

    @property
    def display_emoji(self):
        return "🛒"

    @tasks.loop(minutes=1)
    async def check_effects(self):
        """
        Check if any effect has expired
        """
        for user in self.bot.users:
            if user.bot:
                continue
            account = await bank.Player_Status.get_by_id(user.id)
            for effect in account.effects:
                if not effect.expire_time:
                    continue
                if datetime.now() - effect.expire_time > timedelta(minutes=10):
                    account.effects.remove(effect)
                    logging.info(f"Effect {effect} has expired for {user}")

    @commands.hybrid_group()
    async def shop(self, ctx: commands.Context):
        """Shop commands"""

    @shop.command()
    async def buy(self, ctx: commands.Context, item: Items = None, amount: int = 1):
        """Buy an item"""
        await ctx.defer()
        account = await bank.Player_Status.get_by_id(ctx.author.id)
        if not item:
            embed = discord.Embed(title="Shop", description="Buy an item from the shop")
            for item in Items:
                embed.add_field(
                    name=item.name,
                    value=f"Price: {item.__price__} coins\nDescription: {item.__doc__}",
                )
            await ctx.send(embed=embed)
        money = amount * item.__price__
        if account.money < money:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Error",
                    description=f"You don't have enough coins to buy this item\nExpected: {money} coins\nActual: {account.money} coins",
                    color=discord.Color.red(),
                )
            )
        if amount > 100:
            await ctx.reply(
                embed=discord.Embed(
                    title="Warning",
                    description="You can't buy more than 100 items at once. Fallback to 100 items",
                    color=discord.Color.red(),
                )
            )
            amount = 100
        account.money -= money
        account.inventory.items.extend([item.value for x in range(amount)])
        await ctx.reply(
            embed=discord.Embed(
                title="Success",
                description=f"You have bought {amount} {item.name} for {money} coins",
                color=discord.Color.green(),
            )
        )

    @shop.command()
    async def sell(self, ctx: commands.Context, item: Items, amount: int = 1):
        """
        Sell some items that you bought! (if you are that desperate)
        """
        account = await bank.Player_Status.get_by_id(ctx.author.id)
        if item.value not in account.inventory.items:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Error",
                    description=f"You don't have this item in your inventory",
                    color=discord.Color.red(),
                )
            )
        if amount > account.inventory.items.count(item.value):
            return await ctx.reply(
                embed=discord.Embed(
                    title="Error",
                    description=f"You don't have enough of this item in your inventory",
                    color=discord.Color.red(),
                )
            )
        account.money += (amount * item.__price__) * 0.75
        await ctx.reply(
            embed=discord.Embed(
                title="Success",
                description=f"You have sold {amount} {item.name} for {amount * item.__price__ * 0.75} coins",
                color=discord.Color.green(),
            )
        )

    @shop.command()
    async def send_money(self, ctx: commands.Context, user: discord.User, amount: int):
        """
        Send some money to a user!
        """
        account = await bank.Player_Status.get_by_id(ctx.author.id)
        if account.money < amount:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Error",
                    description=f"You don't have enough coins to send this amount of money",
                    color=discord.Color.red(),
                )
            )
        account.money -= amount
        account = await bank.Player_Status.get_by_id(user.id)
        account.money += amount
        await ctx.reply(
            embed=discord.Embed(
                title="Success",
                description=f"You have sent {amount} coins to {user.mention}",
                color=discord.Color.green(),
            )
        )

    @commands.hybrid_group()
    async def inventory(self, ctx: commands.Context):
        """Inventory commands"""

    @inventory.command()
    async def list(self, ctx: commands.Context):
        """List your inventory"""
        await ctx.defer()
        account = await bank.Player_Status.get_by_id(ctx.author.id)
        counts = {}
        embed = discord.Embed(title="Inventory", description="List of your items")
        for item in account.inventory.items:
            try:
                counts[item] += 1
            except KeyError:
                counts[item] = 1
        for item, count in counts.items():
            doc = None
            if item.effect_name == Items.lucky_potion.value.effect_name:
                doc = Items.lucky_potion.__doc__
            elif item.effect_name == Items.coin_multiplier.value.effect_name:
                doc = Items.coin_multiplier.__doc__
            elif item.effect_name == Items.wipe_effect.value.effect_name:
                doc = Items.wipe_effect.__doc__
            embed.add_field(
                name=item.effect_name.title(),
                value=f"Amount: {count}\nDescription: {doc}",
            )
        await ctx.send(embed=embed)

    @inventory.command()
    async def use(self, ctx: commands.Context, item: Items, game_name=None):
        """Use an item"""
        account = await bank.Player_Status.get_by_id(ctx.author.id)
        item: bank.Effect = item.value
        if item.effect_name not in [
            x.effect_name
            for x in account.inventory.items
            if x.effect_name == item.effect_name
        ]:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Error",
                    description=f"You don't have this item in your inventory",
                    color=discord.Color.red(),
                )
            )
        account.inventory.items.remove(
            random.choice(
                [
                    x
                    for x in account.inventory.items
                    if x.effect_name == item.effect_name
                ]
            )
        )
        if item in [
            x.effect_name for x in account.effects if x.effect_name == item.effect_name
        ]:
            effect = None
            for _effect in account.effects:
                if _effect == item.value:
                    effect = _effect.value
                    break
            if effect.game_name == game_name:
                effect.expire_time = effect.expire_time + timedelta(minutes=10)
            else:
                account.effects.append(item)
                item.activate(game_name)
        elif item == Items.wipe_effect:
            account.unlucky = 0
        else:
            account.effects.append(item)
            item.activate(game_name)
        await ctx.reply(
            embed=discord.Embed(
                title="Success",
                description=f"You have used {item.effect_name}, you can check your effects with `{ctx.prefix}inventory effects`",
                color=discord.Color.green(),
            )
        )

    @inventory.command()
    async def effects(self, ctx: commands.Context):
        """List your effects"""
        await ctx.defer()
        account = await bank.Player_Status.get_by_id(ctx.author.id)
        embed = discord.Embed(title="Effects", description="List of your effects")
        for effect in account.effects:
            doc = None
            if effect.effect_name == Items.lucky_potion.value.effect_name:
                doc = Items.lucky_potion.__doc__
            elif effect.effect_name == Items.coin_multiplier.value.effect_name:
                doc = Items.coin_multiplier.__doc__
            elif effect.effect_name == Items.wipe_effect.value.effect_name:
                doc = Items.wipe_effect.__doc__
            embed.add_field(
                name=effect.effect_name,
                value=f"Description: {doc}\nExpires in: {effect.expire_time - datetime.now()}",
            )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Inventory_And_Shop(bot))
