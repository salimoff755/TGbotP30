from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.states import StepByStepStates, DeveloperState
from main import dp





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

    btns = ['📥 Ohirgi Buyurtma', '📦 Mening Buyurtmalarim', '🔖 Ozim haqimda', '⚙️ Settings', '☎️ Biz bilan boglanish',
            '⬅️ Back']
    markup = make_btn(btns, [1, 2, 2, 1])
    await state.set_state(DevMenu.menu)
    await message.answer("Malumotingiz saqlandi!", reply_markup=markup)