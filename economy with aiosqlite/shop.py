import discord
from discord.ext import commands

shop_items = [
    {"name": "watch", "cost": 100, "id": 1, "info": "It's a watch"},
    {"name": "mobile", "cost": 1000, "id": 2, "info": "It's a mobile"},
    {"name": "laptop", "cost": 10000, "id": 3, "info": "It's a laptop"}
    # You can add your items here ...
]


@client.group(invoke_without_command=True)
@commands.guild_only()
async def shop(ctx):
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
            em.add_field(name=f"{name.upper()} -- {cost}", value=f"{item_info}\nID: `{item_id}`", inline=False)

    await ctx.send(embed=em)


@shop.command(invoke_without_command=True)
@commands.guild_only()
async def info(ctx, *, item_name=None):
    user = ctx.author

    for item in shop_items:
        name = item["name"]
        cost = item["cost"]
        item_info = item["info"]

        if str(name) != str(item_name):
            await ctx.send(f"{user.mention} there's no item named '{item_name}'")
            return

        if str(name) == str(item_name):
            em = discord.Embed(
                description=item_info,
                title=f"{name.upper()}"
            )

            sell_amt = int(cost / 4)

            em.add_field(name="Buying price", value=cost, inline=False)
            em.add_field(name="Selling price", value=sell_amt, inline=False)

            await ctx.send(embed=em)


@client.command()
@commands.guild_only()
async def inventory(ctx):
    user = ctx.author

    await open_inv(user)

    em = discord.Embed(
        color=discord.Color(0x00ff00)
    )

    x = 1

    for item in shop_items:
        name = item["name"]
        item_id = item["id"]

        data = await update_inv(user, 0, str(name))

        if data[0] > 0:
            x += 1

        if x > 1:
            em.add_field(name=f"{name.upper()} - {data[0]}", value=f"ID: {item_id}", inline=False)

    em.set_author(name=f"{user.name}'s Inventory", icon_url=user.avatar_url)

    await ctx.send(embed=em)
