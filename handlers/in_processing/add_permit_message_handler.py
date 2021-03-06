from emoji import emojize

from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp, bot, permit
from states import Processing
from keyboards import create_kb_coustom_main_menu
from utils import notify_about_permit_to_order


@dp.message_handler(state=Processing.add_permit)
async def add_permit_data(message:Message, state:FSMContext):
    data_state = await state.get_data()

    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    request = data_state['chosen_request']
    permit_id = request[1]
    request_numb = request[2]
    permit_date = request[0]
    old_permit_text = permit.get_old_permit_text_or_empty(permit_id)
    new_permit_text = old_permit_text + ' || ' + message.text
    username = message.chat.username

    permit.write_new_permit(permit_id, request_numb, permit_date, permit_text=new_permit_text)

    await notify_about_permit_to_order(request_numb, username)

    await message.answer (
        text='Новый пропуск добавлен, секретарь оповещен!',
        reply_markup=create_kb_coustom_main_menu(message.from_user.id)
    )
    await state.finish()
    # ---> main_menu <---

