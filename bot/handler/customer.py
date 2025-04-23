from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


from bot.handler.developer import make_btn
from bot.main import dp
from bot.states import StepByStepStates, ClientState, ClMenu, CLOrder

@dp.message(StepByStepStates.step1, F.text == '🙋‍♂️ Customer')
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