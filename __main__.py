#!/usr/bin/env python

import argparse
import os
import sys
import copy
import json

from pycolorise.enums import Colors, FontStyles
from pycolorise.colors import *
from pycolorise import Template

WORKING_DIR = os.getcwd() + "\\"

DATABASES = {
    "sqlite": "economy with SQLITE3",
    "aiosqlite": "economy with aiosqlite",
    "mysql": "economy with MYSQL",
    "mongodb": "economy with mongoDB"
}
DATABASE_DIRS = [_ for _ in DATABASES.values()]

T1 = Template(fg=Colors.blue)
T2 = Template(fg=Colors.blue, style=(FontStyles.bold, FontStyles.underline))


def set_database(database: str, rewrite: bool = False):
    with open(WORKING_DIR + "settings.json", 'r+') as f:
        if not rewrite:
            data = json.load(f)
            if data["run"] == database:
                print(T1("Default database is already set to ") + T2(database))
                return

    with open(WORKING_DIR + "settings.json", 'w') as f:
        data = {"run": database}
        f.write(json.dumps(data, indent=2))

    if database == "aiosqlite":
        package = "aiosqlite"
    elif database == "mysql":
        package = "mysql-connector-python"
    elif database == "mongodb":
        package = "pymongo"
    else:
        package = None

    if package is not None:
        try:
            __import__("mysql.connector" if database == "mysql" else package)
        except ModuleNotFoundError:
            if package is not None:
                os.system(f"python -m pip install -U {package}")

    print(T1(f"Default database has been set to"), T2(database))


def run():
    with open(WORKING_DIR + "settings.json", 'r') as f:
        file = json.load(f)["run"]
        if file is None:
            raise RuntimeError("You didn't set a database, set it now using `py . set <database>`")

    os.chdir(WORKING_DIR + DATABASES[file])
    try:
        os.system("python main.py")
    except KeyboardInterrupt:
        print(BrightGreen("\nProcess has been terminated successfully!"))
        exit(1)


def use(database: str, force: str):
    db = DATABASES[database]

    dirs = copy.copy(DATABASE_DIRS)
    dirs.remove(db)

    force = force.upper()
    if force != 'Y':
        agreed = input(BrightRed(
            f"Are you sure you want to delete {', '.join(dirs)} directories?(Y/N)\n>> "
        ))
        if agreed.upper() != 'Y':
            print(T1("process of"), T2("use"), T1("has been terminated!"))
            return

    if sys.platform.startswith("win"):
        cmd = "rmdir /s /q"
    else:
        cmd = "rm -r -f"

    for _dir in dirs:
        if _dir in os.listdir(WORKING_DIR):
            os.system(cmd + f' "{WORKING_DIR + _dir}"')

    set_database(database, True)
    print(T1("Using"), T2(database) + T1(", other database dirs have been removed"))


def reset():
    with open(WORKING_DIR + "settings.json", 'w') as f:
        data = {"run": None}
        f.write(json.dumps(data, indent=2))

    print(T1("settings have been reset successfully"))


def update_git():
    import subprocess

    remote = subprocess.check_output("git remote", shell=True, encoding="utf-8")
    remote = remote.strip()

    branch = subprocess.check_output("git branch", shell=True, encoding="utf-8")
    branch = branch.replace('*', '').strip()
    print(Purple(remote), T1("current Branch:"), T2(branch))

    os.system(f"git pull {remote} {branch}")


def main():
    parser = argparse.ArgumentParser(
        description="command-line funcs"
    )

    commands = parser.add_subparsers(title="Commands")

    install_cmd = commands.add_parser(
        "install", help="installs dependencies from `requirements.txt`"
    )
    install_cmd.set_defaults(func=lambda cmd: install_dependencies())

    set_cmd = commands.add_parser(
        "set", help="sets the selected database as default"
    )
    set_cmd.add_argument(
        "database", type=str,
        choices=[_ for _ in DATABASES.keys()],
        help="sets the provided database"
    )
    set_cmd.set_defaults(func=lambda cmd: set_database(cmd.database))

    run_cmd = commands.add_parser(
        "run", help="runs the default database which has been set"
    )
    run_cmd.set_defaults(func=lambda cmd: run())

    use_cmd = commands.add_parser(
        "use", help="sets the selected database as default and deletes other databases"
    )
    use_cmd.add_argument(
        "database", type=str,
        choices=[_ for _ in DATABASES.keys()],
        help="uses the provided database")
    use_cmd.add_argument(
        "force", type=str,
        help="if 'Y', it will not ask you before deleting the other database dirs"
    )
    use_cmd.set_defaults(func=lambda cmd: use(cmd.database, cmd.force))

    reset_cmd = commands.add_parser(
        "reset", help="resets the settings"
    )
    reset_cmd.set_defaults(func=lambda cmd: reset())

    update_git_cmd = commands.add_parser(
        "update", help="updates your local Git repository with the latest changes from a remote repository"
    )
    update_git_cmd.set_defaults(func=lambda cmd: update_git())

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
