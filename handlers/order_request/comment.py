from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Request
from keyboards import create_kb_send_request
from keyboards import create_kb_send_request_for_change
from keyboards import create_kb_send_request_atm
from utils import get_data_to_show

# from final_step_ordering.py
@dp.message_handler(state=Request.comment)
async def comment(message:types.Message, state:FSMContext):
    await state.update_data(comment=message.text)
    request_data = await state.get_data()

    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=request_data['_del_message']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )    

    result_data_to_show, keyboard = get_data_to_show(request_data)

    await message.answer(text=result_data_to_show, reply_markup=keyboard)

    await Request.type_end.set()
    # to final_step_ordering.py

    return


@dp.callback_query_handler(state=Request.comment)
async def comment_back(call:types.CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    request_data = await state.get_data()

    result_data_to_show, keyboard = get_data_to_show(request_data)

    await call.message.answer(text=result_data_to_show, reply_markup=keyboard)

    await Request.type_end.set()
    # to final_step_ordering.py

    return

    