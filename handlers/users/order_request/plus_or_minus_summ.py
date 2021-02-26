from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state

from loader import dp
from states import Request

@dp.callback_query_handler(state=Request.summ_plus_minus)
async def set_plus_or_minus_summ (
    call:types.CallbackQuery,
    state:FSMContext
):
    data = await state.get_data()

    await call.answer()
    await call.message.delete()
    # call.data = "summ_plus" or "summ_minus"
    await state.update_data(summ_plus_minus=call.data) 
    await call.message.answer('Введите сумму:')
    await Request.adding_summ.set()