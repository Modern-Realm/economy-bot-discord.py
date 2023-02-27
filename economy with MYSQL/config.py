from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=True))


class Auth:
    # Make sure to add all details in '.env' file
    TOKEN = getenv("TOKEN")
    COMMAND_PREFIX = getenv("COMMAND_PREFIX")

    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")
    DB_USER = getenv("DB_USER")
    DB_PASSWD = getenv("DB_PASSWD")
    DB_NAME = getenv("DB_NAME")
