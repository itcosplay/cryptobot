from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Request
from utils import get_data_to_show

# from final_step_ordering.py
@dp.message_handler(state=Request.permit)
async def permit(message:types.Message, state:FSMContext):
    await state.update_data(permit=message.text)
    request_data = await state.get_data()

    await bot.delete_message (
        chat_id = message.chat.id,
        message_id = request_data['_del_message']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )      

    result_data_to_show, keyboard = get_data_to_show(request_data)

    await message.answer(text=result_data_to_show, reply_markup=keyboard)
    await Request.type_end.set()
    # to final_step_ordering.py

    