import sqlite3

file_name = # Enter your file_name here ...

commands_list = ["test", "command1", "command2"] # Enter your command names here !

async def update_plugs():
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS plugins (guildID INTEGER)""")
    db.commit()

    for cdm in commands_list:
        try:
            cursor.execute(f"""ALTER TABLE plugins ADD COLUMN `{cdm}` TEXT DEFAULT 'off'""")
        except:
            pass

    db.commit()

    cursor.close()
    db.close()


async def open_plug(guild):
    await update_plugs()

    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute(f"""SELECT * FROM plugins WHERE guildID = {guild.id}""")
    data = cursor.fetchone()

    if data is None:
        cursor.execute(f"""INSERT INTO plugins(guildID) VALUES({guild.id})""")
        db.commit()

    cursor.close()
    db.close()


async def get_plug(guild, mode):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute(f"""SELECT `{mode}` FROM plugins WHERE guildID = {guild.id}""")
    data = cursor.fetchone()

    cursor.close()
    db.close()

    return data[0]


async def update_plug(guild, button, mode):
    db = sqlite3.connect(file_name)
    cursor = db.cursor()

    cursor.execute(f"""UPDATE plugins SET `{mode}` = '{button}' WHERE guildID = {guild.id}""")
    db.commit()

    cursor.close()
    db.close()
