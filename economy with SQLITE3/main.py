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

	wallet_amt = users[1]
	bank_amt = users[2]

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

    bank_amt = users[2]

    if amount.lower() == "all" or amount.lower() == "max":
        await update_bank(user, +1*bank_amt)
        await update_bank(user, -1*bank_amt, "bank")
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
async def deposit(ctx, *,amount= None):
    user = ctx.author
    await open_account(user)

    users = await get_bank_data(user)

    wallet_amt = users[1]

    if amount.lower() == "all" or amount.lower() == "max":
        await update_bank(user, -1*wallet_amt)
        await update_bank(user, +1*wallet_amt, "bank")
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

@client.command()
@commands.guild_only(aliases=["lb"])
async def leaderboard(ctx):
    users = await get_amt_lb()

    data = []
    index = 1

    for member in users:
        if index > 10:
            break

        member_name = self.client.get_user(member[0])
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
        timestamp=datetime.datetime.utcnow()
    )
    em.set_footer(text=f"GLOBAL - {ctx.guild.name}")
    await ctx.send(embed=em)


client.run(TOKEN)
