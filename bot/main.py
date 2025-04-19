import json

from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder



import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton
from dotenv import load_dotenv

from bot.buttons.reply import make_btn
from bot.states import StepByStepStates

load_dotenv()
TOKEN = getenv('TOKEN')

dp = Dispatcher()








@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    btns = ['📝 Info', '👨‍💻 Developer', '🙋‍♂️ Client']
    sizes = [1, 2]
    markup = make_btn(btns, sizes)
    await state.set_state(StepByStepStates.step1)
    await message.answer(
        f"Assalomu alaykum, {html.bold(message.from_user.full_name)}! Iltimos tugmalardan birini tanlang!",
        reply_markup=markup)


@dp.message(StepByStepStates.step1, F.text == '📝 Info')
async def step_btns_handler(message: Message, state: FSMContext):
    await message.answer('''Bu bot - buyurtmachi va dasturchilarni bir biri bilan boglovchi botdir. 
    Agar siz buyurtmachi bolsangiz sizga qanday dastur yaratish kerak bolsa uni tanlab kerakli dasturchiga yonaltirib beradi.
    Agar siz dasturchi bolsangiz siz qilgan ishlaringizni joylab boring va buyurtmachini toping! 
    ''')








@dp.message(F.text == '⬅️ Back')
async def back_handler(message: Message, state: FSMContext):
    btns = ['📝 Info', '👨‍💻 Developer', '🙋‍♂️ Client']
    sizes = [1, 2]
    markup = make_btn(btns, sizes)
    await state.set_state(StepByStepStates.step1)
    await message.answer("Ortga qaytdingiz. Iltimos, menu tanlang:", reply_markup=markup)




"""
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/salimoff755/TGbotP30.git
git push -u origin main
"""

