from bank_funcs import *
from inventory_funcs import *

import os
import discord

from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv("C:/users/sai keerthan/PyEnvirons/variables.env")

TOKEN = os.getenv("EMOJIS_BOT")  # Enter your Bot Token here !!!
intents = discord.Intents.all()
client = commands.Bot(command_prefix="$", intents=intents)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online)
    print(f"{client.user.name} is online !")


@client.command(aliases=["bal"])
@commands.guild_only()
async def balance(ctx):
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
        color=discord.Color(0x00ff00)
    )

    await ctx.send(embed=em)


@client.command(aliases=["with"])
@commands.guild_only()
async def withdraw(ctx, *, amount=None):
    user = ctx.author
    await open_bank(user)

    users = await get_bank_data(user)

    bank_amt = users[2]

    if amount.lower() == "all" or amount.lower() == "max":
        await update_bank(user, +1 * bank_amt)
        await update_bank(user, -1 * bank_amt, "bank")
        await ctx.send(f"{user.mention} you withdrew {bank_amt} in your wallet")

    bank = users[1]

    amount = int(amount)

    if amount > bank:
        await ctx.send(f"{user.mention} You don't have that enough money!")
        return

    if amount < 0:
        await ctx.send(f"{user.mention} enter a valid amount !")
        return

    await update_bank(user, +1 * amount)
    await update_bank(user, -1 * amount, "bank")

    await ctx.send(f"{user.mention} you withdrew **{amount}** from your **Bank!**")


@client.command(aliases=["dep"])
@commands.guild_only()
async def deposit(ctx, *, amount=None):
    user = ctx.author
    await open_bank(user)

    users = await get_bank_data(user)

    wallet_amt = users[1]

    if amount.lower() == "all" or amount.lower() == "max":
        await update_bank(user, -1 * wallet_amt)
        await update_bank(user, +1 * wallet_amt, "bank")
        await ctx.send(f"{user.mention} you withdrew {wallet_amt} in your wallet")

    amount = int(amount)

    if amount > wallet_amt:
        await ctx.send(f"{user.mention} You don't have that enough money!")
        return

    if amount < 0:
        await ctx.send(f"{user.mention} enter a valid amount !")
        return

    await update_bank(user, -1 * amount)
    await update_bank(user, +1 * amount, "bank")

    await ctx.send(f"{user.mention} you withdrew **{amount}** from your **Bank!**")


@client.command(aliases=["lb"])
@commands.guild_only()
async def leaderboard(ctx):
    users = await get_networth_lb()

    data = []
    index = 1

    for member in users:
        if index > 10:
            break

        member_name = client.get_user(member[0])
        member_amt = member[1]

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


@client.group(invoke_without_command=True)
@commands.guild_only()
async def shop(ctx):
    user = ctx.author

    await open_inv(user)

    em = discord.Embed(
        title="SHOP",
        color=discord.Color(0x00ff00)
    )

    x = 1

    for item in shop_items:
        name = item["name"]
        cost = item["cost"]
        item_id = item["id"]
        item_info = item["info"]

        x += 1

        if x > 1:
            em.add_field(name=f"{name.upper()} -- {cost}", value=f"{item_info}\nID: `{item_id}`", inline=False)

    await ctx.send(embed=em)


@shop.command(invoke_without_command=True)
@commands.guild_only()
async def info(ctx, *, item_name=None):
    user = ctx.author

    for item in shop_items:
        name = item["name"]
        cost = item["cost"]
        item_info = item["info"]

        if str(name) != str(item_name):
            await ctx.send(f"{user.mention} there's no item named '{item_name}'")
            return

        if str(name) == str(item_name):
            em = discord.Embed(
                description=item_info,
                title=f"{name.upper()}"
            )

            sell_amt = int(cost / 4)

            em.add_field(name="Buying price", value=cost, inline=False)
            em.add_field(name="Selling price", value=str(sell_amt), inline=False)

            await ctx.send(embed=em)


@client.command(aliases=["inv"])
@commands.guild_only()
async def inventory(ctx):
    user = ctx.author

    await open_inv(user)

    em = discord.Embed(
        color=discord.Color(0x00ff00)
    )

    x = 1

    for item in shop_items:
        name = item["name"]
        item_id = item["id"]

        data = await update_inv(user, 0, str(name))

        if data[0] > 0:
            x += 1

        if x > 1:
            em.add_field(name=f"{name.upper()} - {data[0]}", value=f"ID: {item_id}", inline=False)

    em.set_author(name=f"{user.name}'s Inventory", icon_url=user.avatar.url)
    if x == 1:
        em.description = "The items which you bought display here..."

    await ctx.send(embed=em)


client.run(TOKEN)
