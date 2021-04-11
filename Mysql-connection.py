# Join our discord server : https://discord.gg/GVMWx5EaAN
# from coder: SKR PHENIX


import discord
from discord.ext import commands
import mysql.connector as Mysql

DB_HOST = "localhost"
DB_USER = # Enter the user name which you created / added in your database (or) just use root as username
DB_PASSWD = # Enter the password of your added user or the root user ( default )
DB_NAME = # Enter your Database Name which you created !

# Remove the below code after creating the table ! ( one-time use )
@client.command()
async def create_table(ctx):
    db = Mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
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

# Remove the above code after creating the table ! ( one-time use )
