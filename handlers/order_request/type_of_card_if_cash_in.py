from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Request
from keyboards import main_menu


# from operation_type.py
@dp.callback_query_handler(state=Request.type_of_card)
async def set_type_of_card(call:types.CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    if call.data == 'exit':
        await call.message.answer (
            f'Создание заявки отменено. Испльзуйте меню\n===========',
            reply_markup=main_menu
        )
        await state.finish()

        return

    await state.update_data(type_of_card=call.data)
    
    result = await call.message.answer(f'укажите сумму:')
    await state.update_data(_del_message=result.message_id)

    await Request.temp_sum_state.set()
    # to temp_sum_message_handler.py