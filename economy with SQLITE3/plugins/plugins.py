import discord
from discord.ext import commands

# Import like this, if the below imported modules/functions didn't work
# Just copy and paste functions from plugins_funcs.py in main.py
from plugins_funcs import open_plug, get_plug, update_plug

TOKEN =  # Enter your bot token here !

intents = discord.Intents.all()

client = commands.Bot(command_prefix="&", intents=intents)
client.remove_command("help")


@client.command()
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def enable(self, ctx, command_name):
    user = ctx.author
    await update_plug(ctx.guild, "on", command_name)
    await ctx.send(f"{user.mention} Plugin-Moderation has been `Enabled`")


@client.command()
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def disable(self, ctx, command_name):
    user = ctx.author
    await update_plug(ctx.guild, "off", command_name)
    await ctx.send(f"{user.mention} Plugin-Moderation has been `Disabled`")


@client.command()
async def test(ctx):
    await open_plug(ctx.guild)
    data = await get_plug(ctx.guild, ctx.command.name)

    # With this process, we can know whether the command is enabled or disabled
    # If the command is enabled, then the command works in that specified server
    # If the command is disabled, then the command will not work in that specified server

    if data == "on":
        await ctx.send("Hello World !")
