# Join our discord server : https://discord.gg/GVMWx5EaAN
# from coder: SKR PHENIX - P.Sai Keerthan Reddy

# make sure to read the instructions in README.md file !!!


from pymongo import MongoClient
import os

auth_url = # paste the url connection of the cluster here !!

shop_items = ["watch", "tv", "mobile"] # You can add as many as items in this list !!!


async def open_bank(user):
    cluster = MongoClient(auth_url)
    db = cluster["my_bot"]

    cursor = db["economy"]

    try:
        post = {"_id": user.id, "wallet": 5000, "bank": 0} # You can add as many columns as you can in this list !!!

        cursor.insert_one(post)

    except:
        pass


async def get_bank_data(user):
    cluster = MongoClient(auth_url)
    db = cluster["my_bot"]

    cursor = db["economy"]

    user_data = cursor.find({"_id": user.id})

    cols = ["wallet", "bank"] # You can add as many columns as you can in this list !!!

    data = []

    for mode in user_data:
        for col in cols:
            data1 = mode[str(col)]

            data.append(data1)

    return data


async def update_bank(user, amount=0, mode="wallet"):
    cluster = MongoClient(auth_url)
    db = cluster["my_bot"]

    cursor = db["economy"]

    cursor.update_one({"_id": user.id}, {"$inc": {str(mode): amount}})

