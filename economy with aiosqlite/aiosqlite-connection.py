# Join our discord server : https://discord.gg/GVMWx5EaAN
# from coder: SKR PHENIX - P.Sai Keerthan Reddy


import discord
from discord.ext import commands
import aiosqlite


file_name = # Enter your file_name which you created (Make sure to crate your file with [.db, .sql, .sqlite3]) , Example: economy.db

# Remove the below code after creating the table !
@client.command()
async def create_table(ctx):
    db = await aiosqlite.connect(file_name)
    cursor = await db.cursor()
    
    cols = ["wallet", "bank"] # You can add as many as columns in this !!!
    
    cursor.execute("""CREATE TABLE economy(userID BIGINT)""")
    await db.commit()
    
    for col in cols:
        cursor.execute(f"ALTER TABLE economy ADD COLUMN {col}")

    await db.commit()

    await cursor.close()
    await db.close()

    await ctx.send("Table created successfully !")

# Remove the above code after creating the table !
