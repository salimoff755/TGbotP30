from aiogram.types import Message

from db.models import User


async def save_user(message):
    user_obj = message.from_user
    user = {
        "id" : user_obj.id,
        "first_name" : user_obj.first_name,
        "last_name" : user_obj.last_name,
        "username" : user_obj.username
    }
    await User.create(**user)

async def check_user(message: Message):
    user = await User.get(id_=message.from_user.id)
    if not user:
        await save_user(message)