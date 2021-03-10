from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from filters import isExecutor_and_higher
from loader import dp

from keyboards.inline.callback_data import get_info_request_data

@dp.callback_query_handler(isExecutor_and_higher(), get_info_request_data.filter(type_btn='GETINFOREQUEST'))
async def rights_users(call:CallbackQuery):
    await call.message.delete()
    await call.message.answer('тут инфа о конкретной заявке')