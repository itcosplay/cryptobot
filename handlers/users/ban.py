from filters.bloked_user import BlokedUser
from aiogram import types

from loader import dp


@dp.message_handler(BlokedUser())
async def ban(message: types.Message):
    return True

