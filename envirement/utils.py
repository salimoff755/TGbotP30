from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Bot:
    TOKEN = getenv("TOKEN")

class DB:
    DB_NAME = getenv("DB_NAME")
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")
    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class Web:
    TOKEN = getenv("WEB_TOKEN")

class Payment:
    CLICK_TOKEN = getenv("CLICK_TOKEN")

class Env:
    bot = Bot()
    db = DB()
    web = Web()
    pay = Payment()
