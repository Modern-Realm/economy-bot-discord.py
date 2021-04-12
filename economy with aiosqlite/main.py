# Join our discord server : https://discord.gg/GVMWx5EaAN
# from coder: SKR PHENIX - P.Sai Keerthan Reddy


import discord
from discord.ext import commands
import asyncio
import aiosqlite


# TOKEN = # Enter your Bot Token here !!!


intents = discord.Intents.all()

client = commands.Bot(command_prefix="&", intents=intents)


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


file_name = "economy.db"


@client.command()
async def create_table(ctx):
    db = await aiosqlite.connect(file_name)
    cursor = await db.cursor()
    
    cols = ["wallet", "bank"] # You can add as many as columns in this !!!
    
    await cursor.execute("""CREATE TABLE economy(userID BIGINT)""")
    await db.commit()
    
    for col in cols:
        await cursor.execute(f"ALTER TABLE economy ADD COLUMN {col}")

    await db.commit()

    await cursor.close()
    await db.close()

    await ctx.send("Table created successfully !")


























client.run(TOKEN)