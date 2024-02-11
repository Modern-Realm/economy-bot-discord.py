# 📙Quickstart

# Method - 1

## clone the repository

```sh
git clone https://github.com/Modern-Realm/economy-bot-discord.py
```

## Setting up the working directory & installing packages

```sh
cd "economy-bot-discord.py/economy with mongoDB"
pip install -r requirements.txt
```

**Note:** make sure to install **any one** of these package`(discord.py, py-cord or nextcord)`

### Provide the secret keys/values in `.env` file

## Running the bot

```sh
python main.py
```

🎉 Your discord bot should be online and ready to use!

# Method - 2

## Download the source file

- [click here](https://github.com/Modern-Realm/economy-bot-discord.py/releases/download/v3.0.7/economy.with.mongoDB.zip)
to download the `zip` file.
- extract all the files & folders

## Install required packages

```shell
pip install -r requirements.txt
```

**Note:** make sure to install **any one** of these package`(discord.py, py-cord or nextcord)`

## Running the bot

```shell
python main.py
```

🎉 Your discord bot should be online and ready to use!

---

# Note: for discord.py users

**You can just clone [`branch:alpha`](https://github.com/Modern-Realm/economy-bot-discord.py/tree/alpha)**

```sh
git clone --single-branch -b alpha https://github.com/Modern-Realm/economy-bot-discord.py
```

**Or make some changes:**

- In `main.py`

  Make sure to uncomment the code where it has `await client.load_extension(...)`.

- In all `*.py` files in `cogs` folder

  Make sure to uncomment the code where the `setup(client)` is asynchronous

  i.e `async def setup(client)`
