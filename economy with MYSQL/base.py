import os
import discord

from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from pycolorise.colors import *

from modules import Database

__all__ = [
    "Auth",
    "EconomyBot"
]

load_dotenv(find_dotenv(raise_error_if_not_found=True))


class Auth:
    # Make sure to add all details in '.env' file
    TOKEN = os.getenv("TOKEN")
    COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWD = os.getenv("DB_PASSWD")
    DB_NAME = os.getenv("DB_NAME")


class EconomyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = Database(
            host=Auth.DB_HOST, port=Auth.DB_PORT,
            username=Auth.DB_USER, passwd=Auth.DB_PASSWD, db_name=Auth.DB_NAME
        )

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
