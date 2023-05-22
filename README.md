# Economy Bot Discord

### • Supports [py-cord](https://github.com/Pycord-Development/pycord), [discord.py](https://github.com/Rapptz/discord.py), [nextcord](https://github.com/nextcord/nextcord)

#### • In this project you will find different code examples of economy bot with various databases.

#### • This module makes the process a lot easier !

[![python badge](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/ "Python")

[![CodeQL](https://github.com/Modern-Realm/economy-bot-discord.py/actions/workflows/codeql.yml/badge.svg)](https://github.com/Modern-Realm/economy-bot-discord.py/actions/workflows/codeql.yml)
[![Generic badge](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.python.org/)
![Github License](https://img.shields.io/badge/license-MIT-blue)
![Windows](https://img.shields.io/badge/os-windows-yellow)
![Linux](https://img.shields.io/badge/os-linux-yellow)

### Join [Official Discord Server](https://discord.gg/GVMWx5EaAN  "click to Join") for more guidance !

<hr/>

## Table of Contents

#### • [Economy with MySQL](https://github.com/Modern-Realm/economy-bot-discord.py/tree/main/economy%20with%20MYSQL)

#### • [Economy with SQLite3](https://github.com/Modern-Realm/economy-bot-discord.py/tree/main/economy%20with%20SQLITE3)

#### • [Economy with AioSQLite](https://github.com/Modern-Realm/economy-bot-discord.py/tree/main/economy%20with%20aiosqlite)

#### • [Economy with MongoDB](https://github.com/Modern-Realm/economy-bot-discord.py/tree/main/economy%20with%20mongoDB)

<br/>

To create a Discord bot using **discord.js**, go
to [economy-bot-discord.js](https://github.com/Modern-Realm/economy-bot-discord.js)

<hr/>

## Thanking JetBrains for Their Support and Assistance

<div align="center">

<img width="90px" height="80px" alt="JetBrains Logo" src="https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.png"/>

<a href="https://jb.gg/OpenSourceSupport">jetbrains.com</a>
Once again thank you 💝 for providing me free OSS License.

These IDE(s) made things a lot easier for us:

• <img height="14px" width="16px" alt="WebStorm logo." src="https://resources.jetbrains.com/storage/products/company/brand/logos/WebStorm_icon.png"/>
**WebStorm** - The smartest JavaScript IDE

• <img height="14px" width="16px" alt="PyCharm logo." src="https://resources.jetbrains.com/storage/products/company/brand/logos/PyCharm_icon.png">
**PyCharm Professional** - Python IDE for professional developers

</div>

<hr/>

## Running the bot

Follow the instructions provided in `README.md` file in each of the database directories.
`Like: economy with SQLITE3`

( or )

Follow the below steps one-by-one, after setting up everything you can run the bot
using the code in **Step-4** directly later on.

**Step-1:** clone the repository

```shell
git clone https://github.com/Modern-Realm/economy-bot-discord.py
```

For [discord.py](https://github.com/Rapptz/discord.py) users, clone using this command

```shell
git clone --single-branch -b alpha https://github.com/Modern-Realm/economy-bot-discord.py
```

**Step-2:** install dependencies

```shell
python -m pip install -r requirements.txt
```

**Step-3:** set the default database

```shell
py . set {database}
```

**Step-4:** run the bot

```shell
py . run
```

**Note:** if you want to delete other database directories, then use below code.
Except the database you provided all other database directories will be deleted.

```shell
py . use {database} {force}
```

`force` - takes either `Y` or `N`. if `Y`, it will not ask you before deleting the other database dirs

`database` - takes values (sqlite, aiosqlite, mysql, mongodb)

use below code for more details

```shell
py .
```

<hr/>

## List of Bot Commands

**`$`** is the default **command prefix**

### • Bank commands

|    Name     | Aliases |      Args      |           Usage           |
|:-----------:|:-------:|:--------------:|:-------------------------:|
|   balance   |   bal   |     member     | `$bal <member: optional>` |
|   deposit   |   dep   |     amount     |      `$dep <amount>`      |
|  withdraw   |  with   |     amount     |     `$with <amount>`      |
|    send     |   ---   | member, amount | `$send <member> <amount>` |
| leaderboard |   lb    |      None      |          `$lb `           |

### • Shop commands

|   Name    | Aliases |   Args    |           Usage           |
|:---------:|:-------:|:---------:|:-------------------------:|
|   shop    |   ---   |   None    |         ` $shop `         |
| shop info |   ---   | item_name |   ` $shop <item name>`    |
|    buy    |   ---   | item_name |    `$buy <item name>`     |
|   sell    |   ---   | item_name |    `$sell <item name>`    |
| inventory |   inv   |  member   | `$inv <member: optional>` |

### • Economy commands

|  Name   | Aliases | Args |   Usage    | Cooldown (in days) |
|:-------:|:-------:|:----:|:----------:|:------------------:|
|  daily  |   ---   | None |  `$daily`  |         1          |
| weekly  |   ---   | None | `$weekly`  |         7          |
| monthly |   ---   | None | `$monthly` |         30         |

### • Admin commands ![Generic badge](https://img.shields.io/badge/new-gold)

|     Name     | Aliases  |         Args         |                     Usage                      |
|:------------:|:--------:|:--------------------:|:----------------------------------------------:|
|  add_money   | addmoney | member, amount, mode | `$addmoney <member> <amount> <mode: optional>` |
| remove_money | remoney  | member, amount, mode | `$remoney <member> <amount> <mode: optional>`  |
|  reset_user  |   ---    |        member        |             `$reset_user <member>`             |

**Note:**
If your bot is not intended for public use`(personal bot)` and is only meant to be used on one or two servers that you
own,
you can add these admin commands.
However, if your bot is publicly available for anyone to add to their server,
it is not recommended to include these admin commands.

### • Fun commands

|   Name    |   Aliases    |      Args      |                Usage                |
|:---------:|:------------:|:--------------:|:-----------------------------------:|
| coin_flip | cf, coinflip | bet_on, amount |       `$cf <bet_on> <amount>`       |
|   slots   |     ---      |     amount     |          `$slots <amount>`          |
|   dice    |     ---      | amount, bet_on | `$dice <amount> <bet_on: optional>` |

New bot commands will be added shortly ...

<hr/>

## Contact Us

- [Discord](https://discord.gg/GVMWx5EaAN) • [Github](https://github.com/skrphenix) • [Gmail](mailto:saikeerthan.keerthan.9@gmail.com)
