from modules import bank_funcs, inventory_funcs
from config import Auth

import os
import discord

from pycolorise.colors import *
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix=Auth.COMMAND_PREFIX, intents=intents, auto_sync_commands=True)


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"{Auth.COMMAND_PREFIX}help")
    )

    # if you are using 'discord.py >=v2.0' comment(remove) below code
    print(Purple("\nLoading Cogs:"))
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            filename = file[:-3]
            try:
                client.load_extension(f"cogs.{filename}")
                print(Blue(f"- {filename} ✅"))
            except:
                print(Blue(f"- {filename} ❌"))

    # if you are using 'discord.py >=v2.0' uncomment(add) below code
    # print(Purple("\nLoading Cogs:"))
    # for file in os.listdir("./cogs"):
    #     if file.endswith(".py"):
    #         filename = file[:-3]
    #         try:
    #             await client.load_extension(f"cogs.{filename}")
    #             print(Blue(f"- {filename} ✅"))
    #         except:
    #             print(Blue(f"- {filename} ❌"))

    print()
    await inventory_funcs.DB.connect()
    if not inventory_funcs.DB.is_connected:
        raise RuntimeError("Database access denied")

    await bank_funcs.create_table()
    await inventory_funcs.create_table()
    print(Cyan("Created/modified tables successfully"))

    print(Cyan(f"{client.user.name} is online !"))


if __name__ == "__main__":
    # Make sure to add Bot Token in '.env' file
    client.run(Auth.TOKEN)
