from config import Auth

import os
import discord

from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix=Auth.command_prefix, intents=intents, auto_sync_commands=True)

client.load_extensions(*(
    f"cogs.{file[:-3]}" for file in os.listdir("./cogs") if file.endswith(".py")
))


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(f"{Auth.command_prefix}help")
    )
    print(f"{client.user.name} is online !")


if __name__ == "__main__":
    # Make sure to add Bot Token in 'secrets.env' file
    client.run(Auth.TOKEN)
