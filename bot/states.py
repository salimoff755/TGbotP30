from aiogram.fsm.state import StatesGroup, State


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