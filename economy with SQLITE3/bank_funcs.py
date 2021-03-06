# Join our discord server : https://discord.gg/GVMWx5EaAN
# from coder: SKR PHOENIX - P.Sai Keerthan Reddy

# make sure to read the instructions in README.md file !!!

import sqlite3

file_name = # Enter your file_name here , with (.db, .sql, .sqlite3) suffix , Example: economy.db

async def open_bank(user):
    columns = ["wallet", "bank"] # You can add more Columns in it !

    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    data = cursor.fetchone()

    if data is None:
        cursor.execute(f"INSERT INTO economy(userID) VALUES({user.id})")
        db.commit()

        for name in columns:
            cursor.execute(f"UPDATE economy SET {name} = 0 WHERE userID = {user.id}")
        db.commit()

        cursor.execute(f"UPDATE economy SET wallet = 5000 WHERE userID = {user.id}")
        db.commit()

    cursor.close()
    db.close()


async def get_bank_data(user):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    users = cursor.fetchone()

    cursor.close()
    db.close()

    return users


async def update_bank(user, amount=0, mode="wallet"):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    data = cursor.fetchone()
    if data is not None:
        cursor.execute(f"UPDATE economy SET {mode} = {mode} + {amount} WHERE userID = {user.id}")
        db.commit()

    cursor.execute(f"SELECT {mode} FROM economy WHERE userID = {user.id}")
    users = cursor.fetchone()

    cursor.close()
    db.close()

    return users


async def get_lb():
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute("SELECT userID, wallet + bank FROM economy ORDER BY wallet + bank DESC")
    users = cursor.fetchall()

    cursor.close()
    db.close()

    return users

