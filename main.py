import discord
from discord.ext import tasks, commands
import asyncio
import random
import time
import os
import datetime
from discord.utils import get
from pymongo import MongoClient
from modules.form_funcs import open_form, get_form_data, update_form

#  ========== SECRET DATA ==========

TOKEN = "Nzc4Mjk0NTEyMjk2Mzk0ODQz.X7P5Pw.fP84mLEgTrSv8x6MXNXWNKY3G-A"

# auth_url = "mongodb+srv://skr:skr.9885543066@cluster0.51vdr.mongodb.net/my_bot?retryWrites=true&w=majority"

extra_items = ["recieved", "sent", "robbed", "robbed_amt", "theft", "theft_amt"]

# TOKEN = os.environ['token']

#  ========== SECRET DATA ==========

coin_icon = "<:pcoins:800002236863217664>"

cod_icon = "<:codcp:800082853525717012>"

tick_icon = "<a:verify_icon:800436350217093170>"

right_icon = "<a:tick_icon:800437907243925535>"

start_time = time.time()
time_now = datetime.datetime.utcnow()
start_date = time_now.strftime("%d")
start_month = time_now.strftime("%B")
start_year = time_now.strftime("%Y")

intents = discord.Intents.all()

client = commands.Bot(command_prefix="&", intents=intents)
client.remove_command("help")

client.load_extension("cogs.mainbank")
client.load_extension("cogs.economy")
client.load_extension("cogs.shop")
client.load_extension("cogs.account")


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("&help - GPE"))
    print("GPE bot is online !")


@client.command()
async def hello(ctx):
    user = ctx.author
    await open_form(user)

    await update_form(user, "Skr Phenix", "username")

    await ctx.send("Hello world !")


@client.command()
@commands.guild_only()
async def uptime(ctx):
    current_time = time.time()

    difference = int(round(current_time - start_time))

    text = str(datetime.timedelta(seconds=difference))

    em = discord.Embed(colour=discord.Color(0xf47fff), timestamp=datetime.datetime.utcnow())

    em.add_field(name="Uptime", value=f"Timer: **`{text}`**", inline=False)

    em.add_field(name="Online since", value=f"{start_month} {start_date}, {start_year}", inline=False)

    em.add_field(name="Hosting-with",
                 value="<:s_heroku:829717546835378256> **[Heroku](https://www.heroku.com/)** - server")

    em.set_author(name=f"{client.user.name} -- BOT", icon_url=client.user.avatar_url)

    em.set_thumbnail(url=client.user.avatar_url)

    em.set_footer(text=ctx.guild.name)

    try:
        await ctx.send(embed=em)
    except discord.HTTPException:
        await ctx.send("Current uptime: " + text)


def convert(seconds: int) -> str:
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:0}hr(s), {minutes:0}min(s) and {seconds:0}sec(s)..."


# @client.event
# async def on_command_error(ctx, error):
# if isinstance(error, commands.CommandOnCooldown):
# msg = f"{ctx.author.mention} I'm tired ! please try again after **{convert(error.retry_after)}**"
# await ctx.send(msg)


client.run(TOKEN)
