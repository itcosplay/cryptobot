from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import message

from loader import dp
from states import Request


# from final_step_ordering.py
@dp.callback_query_handler(state=Request.plus_minus)
async def set_plus_or_minus_summ (
    call:types.CallbackQuery,
    state:FSMContext
):  
    await call.answer()
    await call.message.delete()

    await state.update_data(plus_minus='yes')
    
    ### for logs ### delete later
    request_data = await state.get_data()
    print('=== state: state=Request.plus_minus ===')
    print(request_data)
    print('==============')
    ### for logs ### delete later

    if call.data == 'sum_plus':
        await call.message.answer('Введите сумму:')
        await Request.how_much_recive.set()
        # to how_much_recive.py
    if call.data == 'sum_minus':
        await call.message.answer('Введите сумму:')
        await Request.how_much_give.set()

    

    # await call.message.answer('Введите сумму:')
    # await Request.temp_sum_state.set()
    # # to temp_sum_message_handler.py
