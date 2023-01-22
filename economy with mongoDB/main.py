from modules import bank_funcs, inventory_funcs
from config import Auth

import discord
import os

from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix=Auth.COMMAND_PREFIX, intents=intents)


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"{Auth.COMMAND_PREFIX}help")
    )

    # if you are using 'discord.py >=v2.0' remove below code
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            client.load_extension(f"cogs.{file[:-3]}")

    # if you are using 'discord.py >=v2.0' uncomment(add) below code
    # for file in os.listdir("./cogs"):
    #     if file.endswith(".py"):
    #         await client.load_extension(f"cogs.{file[:-3]}")

    await inventory_funcs.DB.connect()
    if not inventory_funcs.DB.is_connected:
        raise RuntimeError("Database access denied")

    await bank_funcs.create_table()
    await inventory_funcs.create_table()
    print("Created tables successfully")

    print(f"{client.user.name} is online !")


if __name__ == "__main__":
    # Make sure to add Bot Token in '.env' file
    client.run(Auth.TOKEN)
