# Join our discord server : https://discord.gg/GVMWx5EaAN
# from coder: SKR PHOENIX - P.Sai Keerthan Reddy

# make sure to read the instructions in README.md file !!!

file_name = # enter your file name here !

shop_items = [
    {"name": "watch", "cost": 100, "id": 1, "info": "It's a watch"},
    {"name": "mobile", "cost": 1000, "id": 2, "info": "It's a mobile"},
    {"name": "laptop", "cost": 10000, "id": 3, "info": "It's a laptop"}
    # You can add your items here ...
]


async def open_inv(user):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM inventory WHERE userID = {user.id}")
    data = cursor.fetchone()

    if data is None:
        cursor.execute(f"INSERT INTO inventory(userID) VALUES({user.id})")

        for item in shop_items:
            item_name = item["name"]
            cursor.execute(f"UPDATE inventory SET `{item_name}` = 0 WHERE userID = {user.id}")

        db.commit()

    cursor.close()
    db.close()


async def get_inv_data(user):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM inventory WHERE userID = {user.id}")
    users = cursor.fetchone()

    cursor.close()
    db.close()

    return users


async def update_inv(user, amount: int, mode):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM inventory WHERE userID = {user.id}")
    data = cursor.fetchone()

    if data is not None:
        cursor.execute(f"UPDATE inventory SET `{mode}` = `{mode}` + {amount} WHERE userID = {user.id}")
        db.commit()

    cursor.execute(f"SELECT `{mode}` FROM inventory WHERE userID = {user.id}")
    users = cursor.fetchone()

    cursor.close()
    db.close()

    return users