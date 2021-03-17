from datetime import datetime, timedelta
import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Request
from utils import get_data_to_show


# from final_step_ordering.py
@dp.callback_query_handler(state=Request.data_request)
async def set_date_from_buttons (
    call:types.CallbackQuery,
    state:FSMContext
):
    await call.answer()
    await call.message.delete()

    if call.data == 'set_current_date':
        current_date = datetime.today().strftime('%d.%m')
        await state.update_data(data_request=current_date)

    elif call.data == 'set_tomorrow_date':
        tomorrow_date =  (datetime.now() + timedelta(days=1)).strftime("%d.%m")
        await state.update_data(data_request=tomorrow_date)
    
    elif call.data == 'set_after_tomorrow_date':
        after_tomorrow_date = (datetime.now() + timedelta(days=2)).strftime("%d.%m")
        await state.update_data(data_request=after_tomorrow_date)

    else: # call.data == 'enter_coustom_date'
        result = await call.message.answer('Введите дату в формате ЧЧ.ММ')
        await state.update_data(_del_message=result.message_id)
        await state.update_data(data_request='')
        await Request.data_request.set()

        return

    request_data = await state.get_data()
    result_data_to_show, keyboard = get_data_to_show(request_data)

    await call.message.answer(text=result_data_to_show, reply_markup=keyboard)
    await Request.type_end.set()
    # to final_step_ordering.py


@dp.message_handler(state=Request.data_request)
async def set_date_from_text(message:types.Message, state:FSMContext):
    request_data = await state.get_data()
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=request_data['_del_message']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )  
    
    match = re.fullmatch(r'\d\d\.\d\d', message.text)
    
    if match:
        await state.update_data(data_request=message.text)
        request_data = await state.get_data()

        result_data_to_show, keyboard = get_data_to_show(request_data)

        await message.answer(text=result_data_to_show, reply_markup=keyboard)
        await Request.type_end.set()
        # to final_step_ordering.py

    else:
        result = await message.answer('Неправильный формат даты. Попробуйте еще раз ввести в формате чч.мм.\n(пример для 11 ноября: 11.11)')
        await state.update_data(_del_message=result.message_id)
        await state.update_data(data_request='')
        await Request.data_request.set()
        # to THIS HANDLER