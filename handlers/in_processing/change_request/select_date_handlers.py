import re
from datetime import datetime
from datetime import timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from data import all_emoji
from data import sticker
from keyboards import create_kb_chosen_request
from keyboards import create_kb_coustom_main_menu
from loader import bot, dp, sheet
from states import Processing
from utils import get_data_chosen_request
from utils import notify_in_group_chat
from utils import notify_someone



@dp.callback_query_handler(state=Processing.select_date)
async def set_date_from_buttons(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(select_date='+')

    data_state = await state.get_data()
    chosen_request = data_state['chosen_request']
    request_id = chosen_request[2]
    request_type_emoji = all_emoji[chosen_request[3]]
    persone = all_emoji['персона']
    old_date = chosen_request[0]

    if call.data == 'set_tomorrow_date':
        chosen_request[10] = call.message.chat.username
        tomorrow_date =  (datetime.now() + timedelta(days=1)).strftime("%d.%m")
        chosen_request[0] = tomorrow_date
        text = f'{request_type_emoji} #N{request_id}\nизменена дата\n{old_date} 👉 {tomorrow_date}\n{persone} @{chosen_request[10]}'
        
        try:
            result = await call.message.answer_sticker (
                sticker['go_to_table']
            )
            sheet.replace_row(chosen_request)

        except Exception as e:
            print(e)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)
            await call.message.answer_sticker (
                sticker['not_connection']
            )
            await call.message.answer (
                text='Не удалось соединиться с гугл таблицей',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )

            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        await call.message.answer (
            text='Дата заявки изменена',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await notify_someone(text, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text)

        await state.finish()

    elif call.data == 'set_after_tomorrow_date':
        chosen_request[10] = call.message.chat.username
        after_tomorrow_date = (datetime.now() + timedelta(days=2)).strftime("%d.%m")
        chosen_request[0] = after_tomorrow_date
        text = f'{request_type_emoji} #N{request_id}\nизменена дата\n{old_date} 👉 {after_tomorrow_date}\n{persone} @{chosen_request[10]}'

        try:
            result = await call.message.answer_sticker (
                sticker['go_to_table']
            )
            sheet.replace_row(chosen_request)

        except Exception as e:
            print(e)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)
            await call.message.answer_sticker (
                sticker['not_connection']
            )
            await call.message.answer (
                text='Не удалось соединиться с гугл таблицей',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )

            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        await call.message.answer (
            text='Дата заявки изменена',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await notify_someone(text, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text)

        await state.finish()

    elif call.data == 'enter_coustom_date':
        result = await call.message.answer('Введите дату в формате ЧЧ.ММ')

        await state.update_data(message_to_delete=result.message_id)
        await Processing.typing_coustom_date.set()

    elif call.data == 'back_to_request':
        data_state = await state.get_data()
        current_requests = data_state['current_requests']
        chosen_request = data_state['chosen_request']
        request_id = chosen_request[2]

        for request in current_requests:

            if request_id == request[2]:
                await state.update_data(chosen_request=request)

                break

        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']
        text = get_data_chosen_request(chosen_request)

        await call.message.answer (
            text=text,
            reply_markup=create_kb_chosen_request(request)
            # > принято частично (для приема кэша, снятия с карт, обмена)
            # > отложить на выдачу (для доставки, кэшина, обмена)
            # > закрыть заявку
            # > сообщение
            # > изменить заявку
            # > отменить заявку
            # > назад главное меню
        )   
        await Processing.enter_chosen_request_menu.set()

        return

    elif call.data == 'back__main_menu':
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

    chosen_request = data_state['chosen_request']
    request_id = chosen_request[2]
    request_type_emoji = all_emoji[chosen_request[3]]
    persone = all_emoji['персона']
    old_date = chosen_request[0]
    
    match = re.fullmatch(r'\d\d\.\d\d', message.text)
    
    if match:
        chosen_request[10] = message.chat.username
        new_date = message.text
        chosen_request[0] = new_date
        text = f'{request_type_emoji} #N{request_id}\nизменена дата\n{old_date} 👉 {new_date}\n{persone} @{chosen_request[10]}'

        try:
            result = await message.answer_sticker (
                sticker['go_to_table']
            )
            sheet.replace_row(chosen_request)

        except Exception as e:
            print(e)
            await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)
            await message.answer_sticker (
                sticker['not_connection']
            )
            await message.answer (
                text='Не удалось соединиться с гугл таблицей',
                reply_markup=create_kb_coustom_main_menu(message.chat.id)
            )

            return

        await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)

        await message.answer (
            text='Дата заявки изменена',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        
        await notify_someone(text, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text)

        await state.finish()
    else:
        result = await message.answer('Неправильный формат даты. Попробуйте еще раз ввести в формате чч.мм.\n(пример для 11 ноября: 11.11)')
        await state.update_data(message_to_delete=result.message_id)
        await Processing.typing_coustom_date.set()
        # to THIS HANDLER