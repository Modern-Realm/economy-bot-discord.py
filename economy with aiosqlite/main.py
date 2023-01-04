from config import Auth

import os
import discord

from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix=Auth.command_prefix, intents=intents, auto_sync_commands=True)


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"{Auth.command_prefix}help")
    )

    # # if you are using 'discord.py' remove below code
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            client.load_extension(f"cogs.{file[:-3]}")

    # if you are using 'discord.py' uncomment(add) below code
    # for file in os.listdir("./cogs"):
    #     if file.endswith(".py"):
    #         await client.load_extension(f"cogs.{file[:-3]}")

    print(f"{client.user.name} is online !")


if __name__ == "__main__":
    # Make sure to add Bot Token in 'secrets.env' file
    client.run(Auth.TOKEN)
