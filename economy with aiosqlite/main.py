import discord
from base import Auth, EconomyBot

intents = discord.Intents.all()
client = EconomyBot(command_prefix=Auth.COMMAND_PREFIX, intents=intents)

if __name__ == "__main__":
    # Make sure to add Bot Token in '.env' file
    client.run(Auth.TOKEN)
