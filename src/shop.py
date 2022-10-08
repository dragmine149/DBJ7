import logging
from datetime import datetime

import discord
from discord.ext import commands, tasks

from .utils import bank
from .utils.enums import Items


class Inventory_And_Shop(commands.Cog, name="Inventory and shop"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.check_effects.start()
        self.log = logging.getLogger("bot.Inventory_And_Shop")

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
                if datetime.now() - effect.expire_time > datetime.timedelta(minutes=10):
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
        account.money -= money
        for _ in range(amount): # type: ignore
            account.inventory.items.append(item.value)
        await ctx.reply(
            embed=discord.Embed(
                title="Success",
                description=f"You have bought {amount} {item.name} for {money} coins",
                color=discord.Color.green(),
            )
        )

    @shop.command()
    async def sell(self, ctx: commands.Context, item: Items, amount: int = 1):
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
            embed.add_field(
                name=Items(item).name,
                value=f"Amount: {count}\nDescription: {Items(item).__doc__}",
            )
        await ctx.send(embed=embed)
    
    @inventory.command()
    async def use(self, ctx: commands.Context, item: Items):
        """Use an item"""
        account = await bank.Player_Status.get_by_id(ctx.author.id)
        if item.value not in account.inventory.items:
            return await ctx.reply(
                embed=discord.Embed(
                    title="Error",
                    description=f"You don't have this item in your inventory",
                    color=discord.Color.red(),
                )
            )
        account.inventory.items.remove(item.value)
        account.effects.append(item.value)
        item.value.activate()
        await ctx.reply(
            embed=discord.Embed(
                title="Success",
                description=f"You have used {item.name}, you can check your effects with `{ctx.prefix}inventory effects`",
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
            embed.add_field(
                name=Items(effect).name,
                value=f"Description: {Items(effect).__doc__}\nExpires in: {datetime.now() - effect.expire_time}",
            )
        await ctx.send(embed=embed)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(Inventory_And_Shop(bot))
