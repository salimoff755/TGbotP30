
from aiogram.fsm.context import FSMContext
from os import getenv

from aiogram import Dispatcher, F, Router

from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from bot.buttons.reply import make_btn
from bot.states import StepByStepStates
from aiogram.utils.i18n import gettext as _

from bot.utils_functions import check_user
from db.models import User

load_dotenv()
TOKEN = getenv('TOKEN')

dp = Dispatcher()

main_router = Router()






@main_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await check_user(message)
    await message.answer(_("Hello, {}! Please, choose the buttons!".format(message.from_user.full_name)))


@main_router.message(F.text == '🔴 Language')
async def command_start_handler(message: Message, state: FSMContext) -> None:
    btns = ['🇺🇿 Uzbek', '🇷🇺 Russian', '🇬🇧 English']
    sizes = [1, 2]
    markup = make_btn(btns, sizes)
    await state.set_state(StepByStepStates.step1)
    await message.answer(_('Please, choose the languages'),
        reply_markup=markup)


@main_router.message(StepByStepStates.step1, F.text == '📝 Info')
async def step_btns_handler(message: Message, state: FSMContext):
    await message.answer(_('''This bot is a bot that connects customers and developers. 
If you are a customer, it will select the application you need to create and direct you to the right developer. 
If you are a developer, post your work and find a customer.! 
    '''))


@main_router.message(F.text == '⬅️ Back')
async def back_handler(message: Message, state: FSMContext):
    btns = ['📝 Info', '👨‍💻 Developer', '🙋‍♂️ Customer']
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

# btns = ['🔴 Language', '👨‍💻 Developer', '🙋‍♂️ Customer', '📝 Info']