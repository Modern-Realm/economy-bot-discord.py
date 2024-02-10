from modules import Database

import discord
import os

from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
from pycolorise.colors import *

load_dotenv(find_dotenv(raise_error_if_not_found=True))


class Auth:
    # Make sure to add all details in '.env' file
    TOKEN = os.getenv("TOKEN")
    COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
    FILENAME = os.getenv("FILENAME")


class EconomyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = Database(Auth.FILENAME)

    async def on_ready(self):
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(f"{Auth.COMMAND_PREFIX}help")
        )

        # if you are using 'discord.py >=v2.0' comment(remove) below code
        print(Purple("\nLoading Cogs:"))
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                filename = file[:-3]
                try:
                    self.load_extension(f"cogs.{filename}")
                    print(Blue(f"- {filename} ✅ "))
                except:
                    print(Blue(f"- {filename} ❌ "))

        # if you are using 'discord.py >=v2.0' uncomment(add) below code
        # print(Purple("\nLoading Cogs:"))
        # for file in os.listdir("./cogs"):
        #     if file.endswith(".py"):
        #         filename = file[:-3]
        #         try:
        #             await client.load_extension(f"cogs.{filename}")
        #             print(Blue(f"- {filename} ✅ "))
        #         except:
        #             print(Blue(f"- {filename} ❌ "))

        await self.db.bank.create_table()
        await self.db.inv.create_table()
        print(Cyan("Created/modified tables successfully"))

        print(Cyan(f"{self.user.name} is online !"))
