import re

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards import create_kb_change_request
from keyboards import create_kb_coustom_main_menu
from loader import bot, dp
from states import Processing
from utils import get_data_chosen_request
from utils import notify_in_group_chat
from utils import notify_someone


@dp.message_handler(state=Processing.new_request_id)
async def set_date_from_text(message:Message, state:FSMContext):
    data_state = await state.get_data()

    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    match = re.fullmatch(r'\d\d\d\d', message.text)
    
    if match:
        changed_request = data_state['changed_request']

        is_changed = True
        new_numb = message.text

        changed_request[10] = message.chat.username
        changed_request[2] = new_numb

        await state.update_data(is_changed=is_changed)
        await state.update_data(changed_request=changed_request)

        all_changes_data = data_state['all_changes_data']

        if 'numb' not in all_changes_data:
            all_changes_data.append('numb')
            await state.update_data(all_changes_data=all_changes_data)

        text = get_data_chosen_request(changed_request) + \
        '\n\n Выберите изменение:'

        await message.answer (
            text,
            reply_markup=create_kb_change_request(changed_request, is_changed)
        )

        await Processing.change_request_menu.set()

        return

    else:
        result = await message.answer (
            'Неправильный формат номера заявки.' +  ' ' +
            'Попробуйте еще раз ввести в формате XXXX.\n(Например: 1546)'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.new_request_id.set()

        return