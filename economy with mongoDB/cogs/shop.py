from modules.inventory_funcs import *

import discord

from discord.ext import commands


class Shop(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.group()
    @commands.guild_only()
    async def shop(self, ctx):
        user = ctx.author
        await open_inv(user)

        em = discord.Embed(
            title="SHOP",
            color=discord.Color(0x00ff00)
        )
        x = 1
        for item in shop_items:
            name = item["name"]
            cost = item["cost"]
            item_id = item["id"]
            item_info = item["info"]

            x += 1
            if x > 1:
                em.add_field(name=f"{name.upper()} -- {cost}",
                             value=f"{item_info}\nID: `{item_id}`", inline=False)

        await ctx.send(embed=em)

    @shop.command()
    @commands.guild_only()
    async def info(self, ctx, *, item_name: str):
        user = ctx.author
        for item in shop_items:
            name = item["name"]
            cost = item["cost"]
            item_info = item["info"]

            if name != item_name:
                await ctx.send(f"{user.mention} there's no item named '{item_name}'")
                return

            if name == item_name:
                em = discord.Embed(
                    description=item_info,
                    title=f"{name.upper()}"
                )

                sell_amt = int(cost / 4)

                em.add_field(name="Buying price", value=cost, inline=False)
                em.add_field(name="Selling price",
                             value=str(sell_amt), inline=False)

                await ctx.send(embed=em)


# if you are not using 'discord.py >=v2.0' uncomment(add) below code
# def setup(client):
#     client.add_cog(Shop(client))

# if you are not using 'discord.py >=v2.0' comment(remove) below code
async def setup(client):
    await client.add_cog(Shop(client))
