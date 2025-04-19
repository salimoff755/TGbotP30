from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from envirement.utils import Env

TOKEN=Env().bot.TOKEN

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()