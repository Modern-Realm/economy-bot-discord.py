from modules.bank_funcs import *

from numpy import random

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
        await ctx.reply(f"Your daily pocket money is {rand_amt:,}", mention_author=False)

    @commands.cooldown(1, 7 * 24 * 60 * 60)
    @commands.command()
    @commands.guild_only()
    async def weekly(self, ctx):
        user = ctx.author
        await open_bank(user)

        rand_amt = random.randint(7000, 10000)
        await update_bank(user, +rand_amt)
        await ctx.reply(f"Your weekly pocket money is {rand_amt:,}", mention_author=False)

    @commands.cooldown(1, 30 * 24 * 60 * 60)
    @commands.command()
    @commands.guild_only()
    async def monthly(self, ctx):
        user = ctx.author
        await open_bank(user)

        rand_amt = random.randint(30000, 50000)
        await update_bank(user, +rand_amt)
        await ctx.reply(f"Your monthly pocket money is {rand_amt:,}", mention_author=False)


# if you are not using 'discord.py >=v2.0' uncomment(add) below code
# def setup(client):
#     client.add_cog(Economy(client))

# if you are not using 'discord.py >=v2.0' comment(remove) below code
async def setup(client):
    await client.add_cog(Economy(client))
