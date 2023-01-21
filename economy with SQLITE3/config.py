from os import getenv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv("secrets.env", True))


class Auth:
    # Make sure to add all details in 'secrets.env' file
    TOKEN = getenv("TOKEN")
    command_prefix = getenv("COMMAND_PREFIX")
    filename = getenv("DB_NAME")
