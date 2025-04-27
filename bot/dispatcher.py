from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from envirement.utils import Env

TOKEN=Env().bot.TOKEN

# bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()