from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Request


# from final_step_ordering.py
@dp.callback_query_handler(state=Request.sum_plus_minus)
async def set_plus_or_minus_summ (
    call:types.CallbackQuery,
    state:FSMContext
):  
    await call.answer()
    await call.message.delete()
    await state.update_data(sum_plus_minus='ok')

    if call.data == 'sum_plus':
        await state.update_data(addition='sum_plus')
    if call.data == 'sum_minus':
        await state.update_data(substraction='sum_minus')
    ### for logs ### delete later
    request_data = await state.get_data()
    print('=== state: ===')
    print(request_data)
    print('==============')
    ### for logs ### delete later
    await call.message.answer('Введите сумму:')
    await Request.temp_sum_state.set()
    # to temp_sum_message_handler.py
