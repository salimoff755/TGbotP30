

token = '7953079141:AAF_6MOW5U_Nb9uDez5kHsCe9Vg6MSDOWaE'

'''
https://api.telegram.org/bot7953079141:AAF_6MOW5U_Nb9uDez5kHsCe9Vg6MSDOWaE/sendmaessage?chat_id=81255908&text=salom
'''


import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv('TOKEN')

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message(F.text.lower()=='hello')
async def hello_handler(message: Message):
    await message.answer('Qalaysiz')



async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())