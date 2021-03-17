from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import message

from loader import dp
from states import Request
from keyboards import main_menu

# from final_step_ordering.py
@dp.callback_query_handler(state=Request.plus_minus)
async def set_plus_or_minus_summ (
    call:types.CallbackQuery,
    state:FSMContext
):  
    await call.answer()
    await call.message.delete()

    if call.data == 'exit':
        await call.message.answer (
            f'Создание заявки отменено. Испльзуйте меню\n=========================================',
            reply_markup=main_menu
        )
        await state.finish()

        return

    await state.update_data(plus_minus='yes')
    
    if call.data == 'sum_plus':
        result = await call.message.answer('Введите сумму:')
        await Request.how_much_recive.set()
        await state.update_data(_del_message=result.message_id)
        # to how_much_recive.py
    if call.data == 'sum_minus':
        result = await call.message.answer('Введите сумму:')
        await state.update_data(_del_message=result.message_id)
        await Request.how_much_give.set()

    

    # await call.message.answer('Введите сумму:')
    # await Request.temp_sum_state.set()
    # # to temp_sum_message_handler.py
