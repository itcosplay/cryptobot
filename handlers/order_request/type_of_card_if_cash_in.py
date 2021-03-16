from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Request


# from operation_type.py
@dp.callback_query_handler(state=Request.type_of_card)
async def set_type_of_card(call:types.CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(type_of_card=call.data)
    
    result = await call.message.answer(f'укажите сумму:')
    
    await state.update_data(_del_message=result.message_id)
    await Request.temp_sum_state.set()
    # to temp_sum_message_handler.py