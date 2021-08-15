import re
from datetime import datetime
from datetime import timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_change_request
from loader import bot, dp
from states import Processing
from utils import get_data_chosen_request



@dp.callback_query_handler(state=Processing.select_date)
async def set_date_from_buttons (
    call:CallbackQuery, state:FSMContext
):
    await call.answer()
    await call.message.delete()

    data_state = await state.get_data()

    changed_request = data_state['changed_request']

    if call.data == 'set_tomorrow_date':
        tomorrow_date = (
            datetime.now() + timedelta(days=1)
        ).strftime("%d.%m")

        is_changed = True

        changed_request[0] = tomorrow_date
        changed_request[10] = call.message.chat.username
        
        await state.update_data(is_changed=is_changed)
        await state.update_data(changed_request=changed_request)

        text = get_data_chosen_request(changed_request) + \
        '\n\n Выберите изменение:'

        await call.message.answer (
            text,
            reply_markup=create_kb_change_request(changed_request, is_changed)
        )

        await Processing.change_request_menu.set()

        return

    elif call.data == 'set_after_tomorrow_date':
        after_tomorrow_date = (
            datetime.now() + timedelta(days=2)
        ).strftime("%d.%m")

        is_changed = True

        changed_request[10] = call.message.chat.username
        changed_request[0] = after_tomorrow_date

        await state.update_data(is_changed=is_changed)
        await state.update_data(changed_request=changed_request)

        text = get_data_chosen_request(changed_request) + \
        '\n\n Выберите изменение:'

        await call.message.answer (
            text,
            reply_markup=create_kb_change_request(changed_request, is_changed)
        )

        await Processing.change_request_menu.set()

        return

    elif call.data == 'enter_coustom_date':
        result = await call.message.answer('Введите дату в формате ЧЧ.ММ')

        await state.update_data(message_to_delete=result.message_id)
        await Processing.typing_coustom_date.set()

        return

    elif call.data == 'back':
        data_state = await state.get_data()

        changed_request = data_state['changed_request']
        is_changed = data_state['is_changed']

        text = get_data_chosen_request(changed_request) + \
        '\n\n Выберите изменение:'
        
        await call.message.answer (
            text,
            reply_markup=create_kb_change_request(changed_request, is_changed)
        )

        await Processing.change_request_menu.set()

        return

    elif call.data == 'main_menu':
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()
        
        return


@dp.message_handler(state=Processing.typing_coustom_date)
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

    match = re.fullmatch(r'\d\d\.\d\d', message.text)

    if match:
        changed_request = data_state['changed_request']

        is_changed = True
        new_date = message.text

        changed_request[10] = message.chat.username
        changed_request[0] = new_date

        await state.update_data(is_changed=is_changed)
        await state.update_data(changed_request=changed_request)

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
            'Неправильный формат даты.' + \
            ' Попробуйте еще раз ввести в формате чч.мм.\n' + \
            '(пример для 11 ноября: 11.11)'
        )

        await state.update_data(message_to_delete=result.message_id)
        await Processing.typing_coustom_date.set()

        return