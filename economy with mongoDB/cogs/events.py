from config import Auth

import discord

from datetime import timedelta
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        user = ctx.author
        if isinstance(error, commands.errors.CommandNotFound):
            return

        if isinstance(error, commands.errors.MissingRequiredArgument):
            cmd_parent = ctx.command.parent
            if cmd_parent is not None:
                cmd_name = f"{cmd_parent} {ctx.command.name}"
            else:
                cmd_name = ctx.command.name

            cmd_usage = ctx.command.usage
            aliases = ctx.command.aliases
            cmd_params = list(ctx.command.params.values())

            usage = f"{Auth.COMMAND_PREFIX}{cmd_name} "
            if cmd_usage is None:
                cmd_params = cmd_params[2:] if cmd_params[0].name == "self" else cmd_params[1:]
                params = []
                for param in cmd_params:
                    if param.empty:
                        log = f"<{param.name}*>"
                    else:
                        log = f"{param.name}>"
                    params.append(log)

                usage += ' '.join(params)
            else:
                usage += cmd_usage

            em = discord.Embed(
                description=f"**Correct usage**\n`{usage}`"
            )
            if len(aliases) >= 1:
                em.add_field(name="Aliases", value=', '.join(aliases))
            em.set_footer(text="' * ' means that argument is required")
            return await ctx.reply(embed=em, mention_author=False)

        if isinstance(error, commands.errors.CommandOnCooldown):
            time_left = timedelta(seconds=error.retry_after)
            return await ctx.reply(f"You are on cooldown. Try after `{time_left.__str__()}`", mention_author=False)

        raise error


# if you are using 'discord.py >=v2.0' comment(remove) below code
def setup(client):
    client.add_cog(Events(client))

# if you are using 'discord.py >=v2.0' uncomment(add) below code
# async def setup(client):
#     await client.add_cog(Events(client))
