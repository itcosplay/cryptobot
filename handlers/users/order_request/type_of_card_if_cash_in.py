from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from loader import dp
from states import Request


@dp.callback_query_handler(state=Request.type_of_card)
async def set_type_of_card(call:types.CallbackQuery, state:FSMContext):
    await call.answer()

    card = call.data

    await state.update_data(type_of_card=card)
    await call.message.delete()
    await call.message.answer(f'укажите сумму:')
    await Request.how_much.set()