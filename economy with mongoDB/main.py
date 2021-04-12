# Join our discord server : https://discord.gg/GVMWx5EaAN
# from coder: SKR PHENIX - P.Sai Keerthan Reddy

# These are basic codes/commands used for Economy Bot !!!
# make sure to read the instructions in README.md file !!!


import discord
from discord.ext import commands
import asyncio


TOKEN = # Enter your Bot Token here !!!


intents = discord.Intents.all()

client = commands.Bot(command_prefix="skr", intents=intents)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("&help - GPE"))
    print(f"{client.user.name} is online !")



@client.command(aliases=["bal"])
@commands.guild_only()
async def balance(ctx):
	user = ctx.author

	await open_bank(user)

	users = await get_bank_data(user)

	wallet_amt = users[0]
	bank_amt = users[1]

	net_amt = int(wallet_amt + bank_amt)

	em = discord.Embed(
			title= f"{user.name}'s Balance",
			description= f"Wallet: {wallet_amt}\nBank: {bank_amt}",
			color=discord.Color(0x00ff00)
		)

	await ctx.send(embed=em)


@client.command(aliases=["with"])
@commands.guild_only()
async def withdraw(ctx, *,amount= None):
    user = ctx.author
    await open_account(user)

    users = await get_bank_data(user)

    bank_amt = users[1]

    try:
    	if amount.lower() == "all" or amount.lower() == "max":
            await update_bank(user, +1*bank_amt)
            await update_bank(user, -1*bank_amt, "bank")
            await ctx.send(f"{user.mention} you withdrew {bank_amt} in your wallet")
    except:
    	pass

    amount = int(amount)

    if amount > bank_amt:
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
async def deposit(ctx, *,amount= None):
    user = ctx.author
    await open_account(user)

    users = await get_bank_data(user)

    wallet_amt = users[0]

    try:
        if amount.lower() == "all" or amount.lower() == "max":
            await update_bank(user, -1*wallet_amt)
            await update_bank(user, +1*wallet_amt, "bank")
            await ctx.send(f"{user.mention} you withdrew {wallet_amt} in your wallet")
    except:
    	pass

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






















client.run(TOKEN)