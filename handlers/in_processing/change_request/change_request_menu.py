from keyboards.default.admin_keyboard import create_kb_coustom_main_menu
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from data import sticker
from data import all_emoji
from keyboards import cb_change_request
from keyboards import create_kb_change_date
from keyboards import create_kb_chosen_request
from keyboards import create_kb_new_request_type
from keyboards import create_kb_another_currecy_add
from keyboards import create_kb_choose_currency
from loader import dp, bot, sheet, permit
from states import Processing
from utils import get_data_chosen_request
from utils import notify_in_group_chat
from utils import notify_someone
from utils import notify_someone_except_user
from utils import get_text_after_change_request
from utils import updating_log


@dp.callback_query_handler(state=Processing.change_request_menu)
async def change_request_menu_handler(call:CallbackQuery, state:FSMContext):
    '''
    keyboards/inline/in_processin/change_request_keyboards.create_kb_change_request
    > новая дата            new_date
    > новый номер           new_id
    > переопределить тип    change_type
    > изменить сумму        update_sum
    > другая валюта         more_currency
    > СОХРАНИТЬ ИЗМЕНЕНИЯ   save_changes
    > назад                 back
    > главное меню          main_menu
    '''
    await call.answer()
    await call.message.delete()

    data_state = await state.get_data()
    data_btn = cb_change_request.parse(call.data)

    if data_btn['type_btn'] == 'new_date':
        await call.message.answer (
            text='Выберите дату:',
            reply_markup=create_kb_change_date()
        )
        
        await Processing.select_date.set()

        return

    elif data_btn['type_btn'] == 'new_id':
        result = await call.message.answer (
            text='Введите новый номер заявки'
        )
        
        await state.update_data(message_to_delete=result.message_id)
        await Processing.new_request_id.set()

        return

    elif data_btn['type_btn'] == 'change_type':
        data_state = await state.get_data()
        changed_request = data_state['chosen_request']

        await call.message.answer (
            text='Выберите новый тип заявки',
            reply_markup=create_kb_new_request_type()
        )
        await Processing.new_request_type.set()

        return

    elif data_btn['type_btn'] == 'update_sum':
        await call.message.answer (
            text='Выберите валюту',
            reply_markup=create_kb_choose_currency()
        )
        await Processing.which_sum_change__currency.set()

        return

    elif data_btn['type_btn'] == 'save_changes':
        username = call.message.chat.username
        data_state = await state.get_data()

        changed_request = data_state['changed_request']
        changed_request[10] = username
        
        changed_request_id = changed_request[1]
        changed_request_date = changed_request[0]
        changed_request_numb = changed_request[2]

        changed_request[9] = updating_log('CHANGE', username, changed_request)
        
        try:
            result = await call.message.answer_sticker (
                sticker['go_to_table']
            )
            sheet.replace_row(changed_request)

            if 'date' in data_state['all_changes_data']:
                permit.change_permit_date(changed_request_id, changed_request_date)

            if 'numb' in data_state['all_changes_data']:
                permit.change_permit_numb(changed_request_id, changed_request_numb)


            current_requests,\
            in_processing_requests,\
            ready_to_give_requests =\
            sheet.get_numbs_processing_and_ready_requests()

        except Exception as e:
            print(e)
            await bot.delete_message (
                chat_id=call.message.chat.id,
                message_id=result.message_id
            )

            await call.message.answer_sticker (
                sticker['not_connection']
            )

            await call.message.answer (
                text='Не удалось соединиться с гугл таблицей',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )

            return

        await bot.delete_message (
            chat_id=call.message.chat.id,
            message_id=result.message_id
        )

        await state.update_data(current_requests=current_requests)
        await state.update_data(in_processing_requests=in_processing_requests)
        await state.update_data(ready_to_give_requests=ready_to_give_requests)

        for request in current_requests:

            if changed_request_id == request[1]:
                await state.update_data(chosen_request=request)

                break

        text = get_data_chosen_request(changed_request)
        
        await call.message.answer (
            text=text,
            reply_markup=create_kb_chosen_request(changed_request)
            # > принято частично (для приема кэша, снятия с карт, обмена)
            # > отложить на выдачу (для доставки, кэшина, обмена)
            # > закрыть заявку
            # > сообщение
            # > изменить заявку
            # > добавить коментарий
            # > отменить заявку
            # > назад главное меню
        )

        await Processing.enter_chosen_request_menu.set()

        user_id = call.message.chat.id

        change_info_text = get_text_after_change_request (
            data_state['chosen_request'],
            changed_request
        )

        await notify_someone_except_user (
            change_info_text, 
            user_id,
            'admin',
            'changer',
            'executor'
        )
        await notify_in_group_chat(change_info_text)

        return

    elif data_btn['type_btn'] == 'back':
        data_state = await state.get_data()

        chosen_request = data_state['chosen_request']

        text = get_data_chosen_request(chosen_request)
        
        await call.message.answer (
            text=text,
            reply_markup=create_kb_chosen_request(chosen_request)
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

    elif data_btn['type_btn'] == 'main_menu':
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()
        
        return


@dp.message_handler(state=Processing.add_another_comment)
async def add_another_comment(message:Message, state:FSMContext):
    data_state = await state.get_data()
    chosen_request = data_state['chosen_request']

    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    
    if chosen_request[8] != '0':
        comment = chosen_request[8] + ' * '

    else:
        comment = ''

    comment = comment + message.text
    chosen_request[8] = comment

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
        await state.finish()
        return

    await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)

    request_type_emoji = all_emoji[chosen_request[3]]
    request_id = chosen_request[2]
    persone = all_emoji['персона']
    username = message.chat.username

    text = f'{request_type_emoji} #N{request_id}\nдобавлен коментарий\n-----\n{message.text}\n{persone} @{username}'

    await message.answer (
        text='Коментарий добавлен',
        reply_markup=create_kb_coustom_main_menu(message.chat.id)
    )

    await notify_someone(text, 'admin', 'changer', 'executor')
    await notify_in_group_chat(text)

    await state.finish()

    return


@dp.callback_query_handler(state=Processing.add_another_comment)
async def add_another_comment_back(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    data_state = await state.get_data()

    request = data_state['chosen_request']

    text = get_data_chosen_request(request)

    await call.message.answer (
        text=text,
        reply_markup=create_kb_chosen_request(request)
        # > отложить на выдачу (для доставки, кэшина, обмена)
        # > принято частично (для приема кэша, снятия с карт, обмена)
        # > закрыть заявку
        # > сообщение
        # > изменить заявку
        # > добавить пропуск
        # > добавить комментарий
        # > распаковать
        # > отменить заявку
        # > назад
        # > главное меню
    )

    await Processing.enter_chosen_request_menu.set()

    return