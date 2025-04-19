import json

from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from CRUD_DB import *

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

load_dotenv()
TOKEN = getenv('TOKEN')

dp = Dispatcher()


class CLOrder(StatesGroup):
    name = State()
    description = State()
    price = State()
    occupation = State()
    deadline = State()
    tz_file = State()


class DevMenu(StatesGroup):
    menu = State()


class ClMenu(StatesGroup):
    menu = State()


class StepByStepStates(StatesGroup):
    step1 = State()
    dev_step = State()
    cl_step = State()


class ClientState(StatesGroup):
    name = State()
    contact = State()


class DeveloperState(StatesGroup):
    name = State()
    contact = State()
    occupation = State()


def make_btn(btns, sizes):
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[KeyboardButton(text=text) for text in btns])
    rkb.adjust(*sizes)
    return rkb.as_markup(resize_keyboard=True)


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


@dp.message(StepByStepStates.step1, F.text == '👨‍💻 Developer')
async def step_btns_handler(message: Message, state: FSMContext):
    btns = ['Name', 'Contact', 'Occupation', '⬅️ Back']
    markup = make_btn(btns, [2])
    await state.set_state(StepByStepStates.dev_step)
    await message.answer('Iltimos ma"lumotingizni toldiring', reply_markup=markup)


@dp.message(StepByStepStates.dev_step, F.text == 'Name')
async def step2_name_btns_handler(message: Message, state: FSMContext):
    await state.set_state(DeveloperState.name)
    await message.answer('Ismingizni kiriting!')


@dp.message(DeveloperState.name, F.text)
async def dev_name_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(StepByStepStates.dev_step)
    await message.answer('Ismingiz saqlandi!')


@dp.message(StepByStepStates.dev_step, F.text == 'Contact')
async def step2_contact_btns_handler(message: Message, state: FSMContext):
    await state.set_state(DeveloperState.contact)
    await message.answer('Raqamingizni kiriting!')


@dp.message(DeveloperState.contact, F.text)
async def dev_contact_handler(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await state.set_state(StepByStepStates.dev_step)
    await message.answer('Raqamingiz saqlandi!')


@dp.message(StepByStepStates.dev_step, F.text == 'Occupation')
async def step2_occupation_btns_handler(message: Message, state: FSMContext):
    await state.set_state(DeveloperState.occupation)
    await message.answer('Proyeklaringizni kiriting!')


@dp.message(DeveloperState.occupation, F.text)
async def dev_occupation_handler(message: Message, state: FSMContext):
    occupation = message.text
    await state.update_data(occupation=occupation)
    dev_data = await state.get_data()

    try:
        with open("developer.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append({"name": dev_data.get("name", ""),
                 "contact": dev_data.get("contact", ""),
                 "occupation": dev_data.get("occupation", "")})

    with open("developer.json", "w") as f:
        json.dump(data, f, indent=4)

    btns = ['📥 Ohirgi Buyurtma', '📦 Mening Buyurtmalarim', '🔖️ Ozim haqimda', '⚙️ Settings', '☎️ Biz bilan boglanish',
            '⬅️ Back']
    markup = make_btn(btns, [1, 2, 2, 1])
    await state.set_state(DevMenu.menu)
    await message.answer("Malumotingiz saqlandi!", reply_markup=markup)


@dp.message(StepByStepStates.step1, F.text == '🙋‍♂️ Client')
async def step_btns_handler(message: Message, state: FSMContext):
    btns = ['Name', 'Contact', '⬅️ Back']
    markup = make_btn(btns, [2, 1])
    await state.set_state(StepByStepStates.cl_step)
    await message.answer('Iltimos ma"lumotingizni toldiring', reply_markup=markup)


@dp.message(StepByStepStates.cl_step, F.text == 'Name')
async def step2_cl_name_btns_handler(message: Message, state: FSMContext):
    await state.set_state(ClientState.name)
    await message.answer('Ismingizni kiriting!')


@dp.message(ClientState.name, F.text)
async def cl_name_handler(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(StepByStepStates.cl_step)
    await message.answer('Ismingiz saqlandi!')


@dp.message(StepByStepStates.cl_step, F.text == 'Contact')
async def step2_cl_contact_btns_handler(message: Message, state: FSMContext):
    await state.set_state(ClientState.contact)
    await message.answer('Raqamingizni kiriting!')


@dp.message(ClientState.contact, F.text)
async def cl_contact_handler(message: Message, state: FSMContext):
    await state.update_data(contact=message.text)
    cl_data = await state.get_data()
    try:
        with open("customer.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append({"name": cl_data.get("name", "nomalum"),
                 "contact": cl_data.get("contact", "nomalum"),
                 })

    with open("customer.json", "w") as f:
        json.dump(data, f, indent=2)

    btns = ['📤 Buyurtma berish', '📦 Mening Buyurtmalarim', '🔖 Ozim haqimda', '⚙️ Settings', '☎️ Biz bilan boglanish',
            '⬅️ Back']
    markup = make_btn(btns, [1, 2, 2, 1])
    await state.set_state(ClMenu.menu)
    await message.answer("Malumotingiz saqlandi!", reply_markup=markup)


@dp.message(F.text == '📤 Buyurtma berish')
async def clorder_name_handler(message:Message, state:FSMContext):
    await state.set_state(CLOrder.name)
    await message.answer("Proyekt nomini kiriting!")

@dp.message(CLOrder.name, F.text)
async def clorder_name_handler(message: Message, state: FSMContext):
    name = message.text
    await state.update_data({"name": name})
    await state.set_state(CLOrder.description)
    await message.answer("Proyect tavsifini kiriting!")


@dp.message(CLOrder.description, F.text)
async def clorder_description_hanler(message: Message, state: FSMContext):
    description = message.text
    await state.update_data({"description": description})
    await state.set_state(CLOrder.price)
    await message.answer("Project narxini kiring!")


@dp.message(CLOrder.price, F.text)
async def clorder_price_hanler(message: Message, state: FSMContext):
    price = message.text
    await state.update_data({"price": price})
    await state.set_state(CLOrder.deadline)
    await message.answer("Qancha vaqtda bitishi kerak?")


@dp.message(CLOrder.deadline, F.text)
async def clorder_deadline_hanler(message: Message, state: FSMContext):
    deadline = message.text
    await state.update_data({"deadline": deadline})
    await state.set_state(CLOrder.occupation)
    await message.answer("Qaysi dasturlash tilida kerak?")


@dp.message(CLOrder.occupation, F.text)
async def clorder_occupation_hanler(message: Message, state: FSMContext):
    occupation = message.text
    await state.update_data({"occupation": occupation})
    await state.set_state(CLOrder.tz_file)
    await message.answer("Foto korinishida TZ yuboring!")


@dp.message(CLOrder.tz_file, F.photo)
async def clorder_tzfile_hanler(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    clorder_data = await state.get_data()
    clorder_data['file_id'] = file_id
    try:
        with open("cl_order.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(clorder_data)

    with open("cl_order.json", "w") as f:
        json.dump(data, f, indent=4)

    await state.clear()
    await message.answer("✅ Proyekt muvaffaqiyatli saqlandi!")


@dp.message(F.text == '⬅️ Back')
async def back_handler(message: Message, state: FSMContext):
    btns = ['📝 Info', '👨‍💻 Developer', '🙋‍♂️ Client']
    sizes = [1, 2]
    markup = make_btn(btns, sizes)
    await state.set_state(StepByStepStates.step1)
    await message.answer("Ortga qaytdingiz. Iltimos, menu tanlang:", reply_markup=markup)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


"""
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/salimoff755/TGbotP30.git
git push -u origin main
"""

