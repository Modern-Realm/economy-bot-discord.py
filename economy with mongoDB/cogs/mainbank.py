from modules.bank_funcs import *

import discord

from datetime import datetime
from discord.ext import commands


class MainBank(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=["bal"])
    @commands.guild_only()
    async def balance(self, ctx):
        user = ctx.author
        await open_bank(user)

        users = await get_bank_data(user)
        wallet_amt = users[1]
        bank_amt = users[2]
        net_amt = int(wallet_amt + bank_amt)

        em = discord.Embed(
            title=f"{user.name}'s Balance",
            description=f"Wallet: {wallet_amt}\nBank: {bank_amt}\n"
                        f"Net: {net_amt}",
            color=0x00ff00
        )
        await ctx.send(embed=em)

    @commands.command(aliases=["with"])
    @commands.guild_only()
    async def withdraw(self, ctx, amount: str):
        user = ctx.author
        await open_bank(user)

        users = await get_bank_data(user)
        bank_amt = users[2]

        if amount.lower() == "all" or amount.lower() == "max":
            await update_bank(user, +1 * bank_amt)
            await update_bank(user, -1 * bank_amt, "bank")
            return await ctx.send(f"{user.mention} you withdrew {bank_amt:,} in your wallet")

        amount = int(amount)
        if amount > bank_amt:
            await ctx.send(f"{user.mention} You don't have that enough money!")
            return
        if amount < 0:
            await ctx.send(f"{user.mention} enter a valid amount !")
            return

        await update_bank(user, +amount)
        await update_bank(user, -amount, "bank")
        await ctx.send(f"{user.mention} you withdrew {amount:,} from your bank")

    @commands.command(aliases=["dep"])
    @commands.guild_only()
    async def deposit(self, ctx, amount: str):
        user = ctx.author
        await open_bank(user)

        users = await get_bank_data(user)
        wallet_amt = users[1]
        if amount.lower() == "all" or amount.lower() == "max":
            await update_bank(user, -wallet_amt)
            await update_bank(user, +wallet_amt, "bank")
            return await ctx.send(f"{user.mention} you deposited {wallet_amt:,} in your bank")

        amount = int(amount)
        if amount > wallet_amt:
            await ctx.send(f"{user.mention} You don't have that enough money!")
            return
        if amount < 0:
            await ctx.send(f"{user.mention} enter a valid amount !")
            return

        await update_bank(user, -amount)
        await update_bank(user, +amount, "bank")
        await ctx.send(f"{user.mention} you deposited {amount:,} in your bank")

    @commands.command(aliases=["lb"])
    @commands.guild_only()
    async def leaderboard(self, ctx):
        users = await get_networth_lb()

        data = []
        index = 1
        for member in users:
            if index > 10:
                break

            member_name = self.client.get_user(member[0])
            member_amt = member[1] + member[2]

            if index == 1:
                msg1 = f"**🥇 `{member_name}` -- {member_amt}**"
                data.append(msg1)
            if index == 2:
                msg2 = f"**🥈 `{member_name}` -- {member_amt}**"
                data.append(msg2)
            if index == 3:
                msg3 = f"**🥉 `{member_name}` -- {member_amt}**\n"
                data.append(msg3)
            if index >= 4:
                members = f"**{index} `{member_name}` -- {member_amt}**"
                data.append(members)
            index += 1

        msg = "\n".join(data)

        em = discord.Embed(
            title=f"Top {index} Richest Users - Leaderboard",
            description=f"It's Based on Net Worth (wallet + bank) of Global Users\n\n{msg}",
            color=discord.Color(0x00ff00),
            timestamp=datetime.utcnow()
        )
        em.set_footer(text=f"GLOBAL - {ctx.guild.name}")
        await ctx.send(embed=em)


# if you are using 'discord.py >=v2.0' remove below code
def setup(client):
    client.add_cog(MainBank(client))


# if you are using 'discord.py >=v2.0' uncomment(add) below code
# async def setup(client):
#     await client.add_cog(MainBank(client))
