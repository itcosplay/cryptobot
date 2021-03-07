from aiogram import types

from filters import isExecutor_and_higher
from loader import dp, sheet


@dp.message_handler(isExecutor_and_higher(), text='в работе')
async def inter_to_processing(message:types.Message):
    last_row = sheet.get_last_row()
    print(last_row)   
    await message.answer (
        'Тут должно быть меню для текущих заявок'
    )
