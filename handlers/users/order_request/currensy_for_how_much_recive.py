from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from loader import dp
from states import Request


@dp.callback_query_handler(state=Request.how_much_recive_curr)
async def set_how_much_recive_curr (
    call:types.CallbackQuery,
    state:FSMContext
):
    await call.answer()

    currency = call.data

    await state.update_data(how_much_recive_curr=currency)
    await call.message.delete()
    await call.message.answer(f'Сколько выдаем?')
    await Request.how_much_give.set()
