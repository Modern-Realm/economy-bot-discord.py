from modules.bank_funcs import *
from modules.inventory_funcs import *

import discord

from discord.ext import commands


class Inventory(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=["inv"])
    @commands.guild_only()
    async def inventory(self, ctx):
        user = ctx.author
        await open_inv(user)

        em = discord.Embed(color=0x00ff00)
        x = 1
        for item in shop_items:
            name = item["name"]
            item_id = item["id"]

            data = await update_inv(user, 0, name)
            if data >= 1:
                x += 1
                em.add_field(
                    name=f"{name.upper()} - {data}", value=f"ID: {item_id}", inline=False)

        em.set_author(name=f"{user.name}'s Inventory", icon_url=user.avatar.url)
        if x == 1:
            em.description = "The items which you bought display here..."

        await ctx.send(embed=em)

    @commands.command()
    async def buy(self, ctx, *, item_name: str):
        user = ctx.author
        await open_bank(user)
        if item_name.lower() not in [item["name"].lower() for item in shop_items]:
            return await ctx.send(f"{user.mention} theirs no item named `{item_name}`")

        users = await get_bank_data(user)
        for item in shop_items:
            if item_name == item["name"].lower():
                await open_inv(user)
                if users[1] < item["cost"]:
                    return await ctx.send(f"{user.mention} you don't have enough money to buy {item['name']}")

                await update_inv(user, +1, item["name"])
                await update_bank(user, -item["cost"])
                return await ctx.send(f"{user.mention} you bought {item_name}")

    @commands.command()
    async def sell(self, ctx, *, item_name: str):
        user = ctx.author
        await open_bank(user)
        if item_name.lower() not in [item["name"].lower() for item in shop_items]:
            return await ctx.send(f"{user.mention} theirs no item named `{item_name}`")

        for item in shop_items:
            if item_name.lower() == item["name"].lower():
                cost = int(round(item["cost"] / 2, 0))
                quantity = await update_inv(user, 0, item["name"])
                if quantity < 1:
                    return await ctx.send(f"{user.mention} you don't have {item['name']} in your inventory")

                await open_inv(user)
                await update_inv(user, -1, item["name"])
                await update_bank(user, +cost)
                return await ctx.send(f"{user.mention} you sold {item_name} for {cost:,}")


# if you are using 'discord.py >=v2.0' remove below code
def setup(client):
    client.add_cog(Inventory(client))


# if you are using 'discord.py >=v2.0' uncomment(add) below code
# async def setup(client):
#     await client.add_cog(Inventory(client))
