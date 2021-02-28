from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiohttp.client import request

from loader import dp, bot
from states import Request
from keyboards import create_kb_smart_choose_curr


# from operation_type.py
# from plus_or_minus.py
@dp.message_handler(state=Request.how_much_recive)
async def set_how_much_recive(message:types.Message, state:FSMContext):
    try:
        summ = float(message.text)
        await state.update_data(how_much_recive=summ)
        request_data = await state.get_data()
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id - 1
        )
        await bot.delete_message (
            chat_id=message.chat.id,
            message_id=message.message_id
        )        
        await message.answer (
            f'Выберете валюту:',
            reply_markup=create_kb_smart_choose_curr(request_data['currencies__recive'])
        )
        await Request.currency__how_much__recive.set()
        # to currency__how_much__recive.py

    except Exception:
        await message.answer (
            f'Формат суммы неправильный. Создание заявки отменено.'
        )
        await state.finish()
        await message.delete()