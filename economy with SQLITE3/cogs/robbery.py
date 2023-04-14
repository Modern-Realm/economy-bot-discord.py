import discord

from modules.bank_funcs import *

from numpy import random

from discord.ext import commands


class Robbery(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=["steal"], usage="<member*: @member>")
    async def rob(self, ctx, member: discord.Member):
        user = ctx.author
        if member == user:
            return await ctx.reply("You can't rob yourself", mention_author=False)
        if member.bot:
            return await ctx.reply("You can't rob a bot", mention_author=False)

        await open_bank(member)
        users = await get_bank_data(member)

        rand_percent = random.randint(range(1, 5))
        wallet_amt = users[1] * (rand_percent / 10)
        if wallet_amt < 1000:
            return await ctx.reply(
                f"`{member}` doesn't have enough money, you can't rob this member",
                mention_author=False
            )

        rand_amt = random.randint(min(100, wallet_amt), wallet_amt)
        await update_bank(user, +rand_amt)
        await update_bank(member, -rand_amt)

        await ctx.reply(
            f"You robbed {rand_amt:,} from {member.mention}",
            mention_author=False
        )

    @commands.command(aliases=["robbank", "stealbank"], usage="<member*: @member>")
    async def rob_bank(self, ctx, member: discord.Member):
        user = ctx.author

        # code here


# if you are using 'discord.py >=v2.0' comment(remove) below code
def setup(client):
    client.add_cog(Robbery(client))

# if you are using 'discord.py >=v2.0' uncomment(add) below code
# async def setup(client):
#     await client.add_cog(Robbery(client))
