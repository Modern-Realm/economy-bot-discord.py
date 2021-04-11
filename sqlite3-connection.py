# Join our discord server : https://discord.gg/GVMWx5EaAN
# from coder: SKR PHENIX - Sai Keerthan Reddy


import discord
from discord.ext import commands
import sqlite3


file_name = # Enter your file_name which you created (Make sure to crate your file with [.db, .sql, .sqlite3]) , Example: economy.db

# Remove the below code after creating the table !
@client.command()
async def create_table(ctx):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    
    cols = ["wallet", "bank"] # You can add as many as columns in this !!!
    
    cursor.execute("""CREATE TABLE economy(userID BIGINT)""")
    db.commit()
    
    for col in cols:
        cursor.execute(f"ALTER TABLE economy ADD COLUMN {col}")

    db.commit()

    cursor.close()
    db.close()

    await ctx.send("Table created successfully !")

# Remove the above code after creating the table !
