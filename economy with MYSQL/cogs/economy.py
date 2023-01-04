from modules.bank_funcs import *

import random

from datetime import timedelta
from discord.ext import commands


class Economy(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.cooldown(1, 24 * 60 * 60)
    @commands.command()
    @commands.guild_only()
    async def daily(self, ctx):
        user = ctx.author
        await open_bank(user)

        rand_amt = random.randint(3000, 5000)
        await update_bank(user, +rand_amt)
        await ctx.send(f"{user.mention} your daily pocket money is {rand_amt:,}")

    @commands.cooldown(1, 7 * 24 * 60 * 60)
    @commands.command()
    @commands.guild_only()
    async def weekly(self, ctx):
        user = ctx.author
        await open_bank(user)

        rand_amt = random.randint(7000, 10000)
        await update_bank(user, +rand_amt)
        await ctx.send(f"{user.mention} your weekly pocket money is {rand_amt:,}")

    @commands.cooldown(1, 30 * 24 * 60 * 60)
    @commands.command()
    @commands.guild_only()
    async def monthly(self, ctx):
        user = ctx.author
        await open_bank(user)

        rand_amt = random.randint(30000, 50000)
        await update_bank(user, +rand_amt)
        await ctx.send(f"{user.mention} your monthly pocket money is {rand_amt:,}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        user = ctx.author
        if isinstance(error, commands.CommandOnCooldown):
            time_left = str(timedelta(seconds=error.retry_after))
            return await ctx.send(f"{user.mention} you are on cooldown. Try after `{time_left}`")


# if you are using 'discord.py >=v2.0' remove below code
def setup(client):
    client.add_cog(Economy(client))


# if you are using 'discord.py >=v2.0' uncomment(add) below code
# async def setup(client):
#     await client.add_cog(Economy(client))
