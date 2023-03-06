from modules.bank_funcs import *

import discord
import asyncio

from typing import List
from numpy import random
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=["cf", "coinflip"], usage="<bet_on*: heads(H) or tails(T)> <amount*: integer>")
    @commands.guild_only()
    async def coin_flip(self, ctx, bet_on: str, amount: int):
        user = ctx.author
        await open_bank(user)

        bet_on = "heads" if "h" in bet_on.lower() else "tails"
        if not 500 <= amount <= 5000:
            return await ctx.reply("You can only bet amount between 500 and 5000", mention_author=False)

        reward = round(amount / 2)
        users = await get_bank_data(user)
        if users[1] < amount:
            return await ctx.reply("You don't have enough money", mention_author=False)

        coin = ["heads", "tails"]
        result = random.choice(coin)

        if result != bet_on:
            await update_bank(user, -amount)
            return await ctx.reply(f"Got {result}, you lost {amount:,}", mention_author=False)

        await update_bank(user, +reward)
        return await ctx.reply(f"Got {result}, you won {amount + reward:,}", mention_author=False)

    @commands.command(usage="<amount*: integer")
    @commands.guild_only()
    async def slots(self, ctx: commands.Context, amount: int):
        user = ctx.author
        await open_bank(user)
        if not 1000 <= amount <= 10000:
            return await ctx.reply("You can only bet amount between 1000 and 10000", mention_author=False)

        users = await get_bank_data(user)
        if users[1] < amount:
            return await ctx.reply("You don't have enough money", mention_author=False)

        slot1 = ["💝", "🎉", "💎", "💵", "💰", "🚀", "🍿"]
        slot2 = ["💝", "🎉", "💎", "💵", "💰", "🚀", "🍿"]
        slot3 = ["💝", "🎉", "💎", "💵", "💰", "🚀", "🍿"]
        sep = " | "

        em = discord.Embed(
            description=f"```\n"
                        f"| {sep.join(slot1[:3])} |\n"
                        f"| {sep.join(slot2[:3])} | 📍\n"
                        f"| {sep.join(slot3[:3])} |\n"
                        f"```"
        )
        msg = await ctx.reply(content="spinning the slot", embed=em, mention_author=False)
        await asyncio.sleep(3)

        total = len(slot1)
        if total % 2 == 0:  # if even
            mid = total / 2
        else:
            mid = (total + 1) // 2

        random.shuffle(slot1)
        random.shuffle(slot2)
        random.shuffle(slot3)
        result: List[List[str]] = []
        for x in range(total):
            result.append([slot1[x], slot2[x], slot3[x]])

        em = discord.Embed(
            description=f"```\n"
                        f"| {sep.join(result[mid - 1])} |\n"
                        f"| {sep.join(result[mid])} | 📍\n"
                        f"| {sep.join(result[mid + 1])} |\n"
                        f"```"
        )

        slot = result[mid]
        s1 = slot[0]
        s2 = slot[1]
        s3 = slot[2]
        if s1 == s2 == s3:
            reward = round(amount / 2)
            await update_bank(user, +reward)
            content = f"{user.mention} Jackpot! you won {amount + reward:,}"
        elif s1 == s2 or s2 == s3 or s1 == s3:
            reward = round(amount / 4)
            await update_bank(user, +reward)
            content = f"{user.mention} GG! you only won {amount + reward:,}"
        else:
            await update_bank(user, -amount)
            content = f"{user.mention} You lost {amount:,}"

        return await msg.edit(content=content, embed=em)

    @commands.command(usage="<amount*: integer> <bet_on: integer>")
    async def dice(self, ctx, amount: int, bet_on: int = 6):
        user = ctx.author
        await open_bank(user)

        rdice = [1, 2, 3, 4, 5, 6]
        if bet_on not in rdice:
            return await ctx.reply("Enter a number of dice(1 - 6)", mention_author=False)

        if not 1000 <= amount <= 5000:
            return await ctx.reply("You can only bet amount between 1000 and 5000", mention_author=False)

        users = await get_bank_data(user)
        if users[1] < amount:
            return await ctx.reply("You don't have enough money", mention_author=False)

        rand_num = random.choice(rdice)
        if rand_num != bet_on:
            await update_bank(user, -amount)
            return await ctx.reply(f"Got {rand_num}, you lost {amount:,}", mention_author=False)

        reward = round(amount / 2)
        await update_bank(user, +reward)
        await ctx.reply(f"Got {rand_num}, you won {amount + reward:,}", mention_author=False)


# if you are not using 'discord.py >=v2.0' uncomment(add) below code
# def setup(client):
#     client.add_cog(Fun(client))

# if you are not using 'discord.py >=v2.0' comment(remove) below code
async def setup(client):
    await client.add_cog(Fun(client))
