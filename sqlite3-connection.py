# Join our discord server : https://discord.gg/GVMWx5EaAN
# from coder: SKR PHENIX - Sai Keerthan Reddy


import discord
from discord.ext import commands
import sqlite3


file_name = # Enter your file_name which you created (Make sure to crate your file with [.db, .sql, .sqlite3]) !

# Remove the below code after creating the table !
@client.command()
async def create_table(ctx):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE economy(
      userID BIGINT,
      wallet INT,
      bank INT
    )
    """)
    db.commit()

    cursor.close()
    db.close()

    await ctx.send("Table created successfully !")

# Remove the above code after creating the table !
