from emoji import emojize

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, bot, 
from states import Processing



@dp.message_handler(state=Processing.correct_amount_sum_ready)
async def set_sum_to_correct(message:Message, state:FSMContext):

    data_state = await state.get_data()
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    new_permit_text = message.text

    old_permit_text = request[]


    await Processing.confirm_correct_to_ready.set()
    # to chosen_request_menu.py

