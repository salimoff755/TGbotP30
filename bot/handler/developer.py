from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


from bot.buttons.reply import make_btn
from bot.states import StepByStepStates, DeveloperState, DevMenu
from db.model import Manager
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

    developer = Manager()
    developer.name = dev_data.get('name')
    developer.contact = dev_data.get('contact')
    developer.occupation = dev_data.get('occupation')

    dev_save = developer.save()  # Hech qanday try-except yo‘q

    if dev_save:
        btns = ['📥 Ohirgi Buyurtma', '📦 Mening Buyurtmalarim', '🔖 Ozim haqimda', '⚙️ Settings',
                '☎️ Biz bilan boglanish', '⬅️ Back']
        markup = make_btn(btns, [1, 2, 2, 1])
        await state.set_state(DevMenu.menu)
        await message.answer("Ma'lumotingiz muvaffaqiyatli saqlandi!", reply_markup=markup)
    else:
        await message.answer("Ma'lumot saqlanmadi. Iltimos, qaytadan urinib ko'ring.")
