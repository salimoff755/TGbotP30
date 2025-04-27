from bot.dispatcher import dp
from bot.handler.main import *
from bot.handler.admin import *
from bot.handler.customer import *
from bot.handler.developer import *
from bot.handler.project_router import *
from bot.main import main_router

dp.include_router(
    *[main_router]
)