# Join our discord server : https://discord.gg/GVMWx5EaAN
# from coder: SKR PHOENIX - P.Sai Keerthan Reddy

# make sure to read the instructions in README.md file !!!

file_name = # enter your file name here !


async def open_bank(user):
    columns = ["wallet", "bank"] # You can add more Columns in it !

    db = await aiosqlite.connect(file_name)
    cursor = await db.cursor()
    await cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    data = await cursor.fetchone()

    if data is None:
        await cursor.execute(f"INSERT INTO economy(userID) VALUES({user.id})")
        await db.commit()

        for name in columns:
            await cursor.execute(f"UPDATE economy SET {name} = 0 WHERE userID = {user.id}")
        await db.commit()

        await cursor.execute(f"UPDATE economy SET wallet = 5000 WHERE userID = {user.id}")
        await db.commit()

    await cursor.close()
    await db.close()


async def get_bank_data(user):
    db = await aiosqlite.connect(file_name)
    cursor = await db.cursor()
    await cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    users = await cursor.fetchone()

    await cursor.close()
    await db.close()

    return users


async def update_bank(user, amount=0, mode="wallet"):
    db = await aiosqlite.connect(file_name)
    cursor = await db.cursor()

    await cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    data = await cursor.fetchone()
    if data is not None:
        await cursor.execute(f"UPDATE economy SET {mode} = {mode} + {amount} WHERE userID = {user.id}")
        await db.commit()

    await cursor.execute(f"SELECT {mode} FROM economy WHERE userID = {user.id}")
    users = await cursor.fetchone()

    await cursor.close()
    await db.close()

    return users


async def get_lb():
    db = await aiosqlite.connect(file_name)
    cursor = await db.cursor()

    await cursor.execute("SELECT userID, wallet + bank FROM economy ORDER BY wallet + bank DESC")
    users = await cursor.fetchall()

    await cursor.close()
    await db.close()

    return users

