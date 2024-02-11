from base import EconomyBot

import discord

from discord.ext import commands


class Inventory(commands.Cog):
    def __init__(self, client: EconomyBot):
        self.client = client
        self.bank = self.client.db.bank
        self.inv = self.client.db.inv

    @commands.command(aliases=["inv"], usage="<member: @member>")
    @commands.guild_only()
    async def inventory(self, ctx, member: discord.Member = None):
        user = member or ctx.author
        user_av = user.display_avatar or user.default_avatar
        if user.bot:
            return await ctx.reply("Bot's don't have account", mention_author=False)
        await self.bank.open_acc(user)

        em = discord.Embed(color=0x00ff00)
        x = 1
        for item in self.inv.shop_items:
            name = item["name"]
            item_id = item["id"]

            data = await self.inv.update_acc(user, 0, name)
            if data[0] >= 1:
                x += 1
                em.add_field(
                    name=f"{name.upper()} - {data[0]}", value=f"ID: {item_id}", inline=False)

        em.set_author(name=f"{user.name}'s Inventory", icon_url=user_av.url)
        if x == 1:
            em.description = "The items which you bought display here..."

        await ctx.reply(embed=em, mention_author=False)

    @commands.command(usage="<item_name*: string>")
    async def buy(self, ctx, *, item_name: str):
        user = ctx.author
        await self.bank.open_acc(user)
        await self.inv.open_acc(user)

        if item_name.lower() not in [item["name"].lower() for item in self.inv.shop_items]:
            return await ctx.reply(f"Theirs no item named `{item_name}`", mention_author=False)

        users = await self.bank.get_acc(user)
        for item in self.inv.shop_items:
            if item_name == item["name"].lower():
                if users[1] < item["cost"]:
                    return await ctx.reply(f"You don't have enough money to buy {item['name']}",
                                           mention_author=False)

                await self.inv.update_acc(user, +1, item["name"])
                await self.bank.update_acc(user, -item["cost"])
                return await ctx.reply(f"You bought {item_name}", mention_author=False)

    @commands.command(usage="<item_name*: string>")
    async def sell(self, ctx, *, item_name: str):
        user = ctx.author
        await self.bank.open_acc(user)
        await self.inv.open_acc(user)

        if item_name.lower() not in [item["name"].lower() for item in self.inv.shop_items]:
            return await ctx.reply(f"Theirs no item named `{item_name}`", mention_author=False)

        for item in self.inv.shop_items:
            if item_name.lower() == item["name"].lower():
                cost = int(round(item["cost"] / 2, 0))
                quantity = await self.inv.update_acc(user, 0, item["name"])
                if quantity[0] < 1:
                    return await ctx.reply(f"You don't have {item['name']} in your inventory",
                                           mention_author=False)

                await self.inv.update_acc(user, -1, item["name"])
                await self.bank.update_acc(user, +cost)
                return await ctx.reply(f"You sold {item_name} for {cost:,}", mention_author=False)


# if you are using 'discord.py >=v2.0' comment(remove) below code
def setup(client):
    client.add_cog(Inventory(client))

# if you are using 'discord.py >=v2.0' uncomment(add) below code
# async def setup(client):
#     await client.add_cog(Inventory(client))
