from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv("secrets.env", True))


class Auth:
    # Make sure to add all details in 'secrets.env' file
    TOKEN = getenv("TOKEN")
    command_prefix = getenv("COMMAND_PREFIX")

    DB_HOST = getenv("DB_HOST")
    DB_USER = getenv("DB_USER")
    DB_PASSWD = getenv("DB_PASSWD")
    DB_NAME = getenv("DB_NAME")
