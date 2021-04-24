import data
import traceback
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery

from data import sticker
from data import all_emoji
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_change_sum_finished_req
from keyboards import cb_change_finished_req
from keyboards import cb_finished_requests
from keyboards import create_kb_change_fin_request
from keyboards import create_kb_another_currecy_add_fin
from keyboards import cb_anoter_currency_add_fin
from loader import dp, sheet, bot
from states import Reportsstate
from utils import notify_in_group_chat
from utils import notify_someone
from utils import notify_in_group_chat
from utils import get_data_finished_request


@dp.callback_query_handler(state=Reportsstate.return_request_menu)
async def show_finished_request(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(return_request_menu='+')

    data_btn = cb_finished_requests.parse(call.data)

    if data_btn['type_btn'] == 'exit':
        await call.message.answer (
            text='Выход из меню "ОТЧЕТНОСТЬ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()
        
        return

    data_state = await state.get_data()
    finished_requests = data_state['finished_requests']

    for request in finished_requests:

        if data_btn['id'] == request[1]:
            await state.update_data(chosen_request=request)

            break

    data_state = await state.get_data()
    request = data_state['chosen_request']
    text = get_data_finished_request(request)

    await call.message.answer (
        text=text,
        reply_markup=create_kb_change_fin_request()
    )

    await Reportsstate.change_fin_request.set()

    return


@dp.callback_query_handler(state=Reportsstate.change_fin_request)
async def change_menu_finished_req(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(change_fin_request='+')

    data_state = await state.get_data()
    chosen_request = data_state['chosen_request']

    if call.data == 'add_another_curr':
        await call.message.answer (
            text='Выберите вылюту, которую хотите добавить',
            reply_markup=create_kb_another_currecy_add_fin(chosen_request)
        )

        await Reportsstate.set_new_curr.set()

        return


    if call.data == 'change_sum':
        await call.message.answer (
            text='Выберите cумму, которую хотите изменить',
            reply_markup=create_kb_change_sum_finished_req(chosen_request)
        )

        await Reportsstate.set_change_curr.set()

        return

    elif call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "ОТЧЕТНОСТЬ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return

# ДОБАВЛЯЕМ НОВУЮ ВАЛЮТУ
@dp.callback_query_handler(state=Reportsstate.set_new_curr)
async def set_new_curr_finished_req(call:CallbackQuery, state:FSMContext):
    '''
    - RUB
    - USD
    - EUR
    - back_main_menu
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(set_new_curr='+')

    data_btn = cb_anoter_currency_add_fin.parse(call.data)

    if data_btn['type_btn'] == 'add_curr':
        await state.update_data(new_curr=data_btn['curr'])

        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        if chosen_request[3] == 'выдача в офисе' or chosen_request[3] == 'доставка' or chosen_request[3] == 'кэшин':
            await state.update_data(new_curr_sign='-')

        else:
            await state.update_data(new_curr_sign='')

        result = await call.message.answer (
            text='Введите сумму'
        )
        await state.update_data(message_to_delete=result.message_id)
        
        await Reportsstate.add_curr_amount.set()

        return

    else:
        await call.message.answer (
            text='Выход из меню "Отчетность". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return

# ДОБАВЛЯЕМ НОВУЮ ВАЛЮТУ
@dp.message_handler(state=Reportsstate.add_curr_amount)
async def set_sum_return(message:Message, state:FSMContext):
    data_state = await state.get_data()
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    try:
        sum_amount = int(message.text)
        
        if sum_amount <= 0:
            raise ValueError('fuck off')
        sum_amount = str(sum_amount)
        
    except Exception as e:
        print(e)
        traceback.print_exception()

        await message.answer (
            text='Изменение заявки отменено. Формат суммы не правильный.',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        
        await state.finish()

        return

    new_curr = data_state['new_curr']
    new_curr_sign = data_state['new_curr_sign']
    full_new_sum = new_curr_sign + message.text
    chosen_request = data_state['chosen_request']

    if new_curr == 'rub':
        chosen_request[5] = full_new_sum

    if new_curr == 'usd':
        chosen_request[6] = full_new_sum

    if new_curr == 'eur':
        chosen_request[7] = full_new_sum

    chosen_request[11] = 'В обработке'
    chosen_request[15] = '0'
    chosen_request[16] = '0'
    username = message.chat.username
    chosen_request[10] = username

    old_comment = chosen_request[8]
    chosen_request[8] = old_comment + f' * возвращена в обработку с новой валютой ({new_curr})'

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
    request_numb = chosen_request[2]
    persone = all_emoji['персона']
    request_date = chosen_request[0]
    text = f'{request_type_emoji} #N{request_numb} от {request_date}\nвозвращена в обработку с новой валютой\n{persone} @{username}'

    await message.answer (
        text='Сумма в новой валюте добавлена, заявка возвращена в обработку!',
        reply_markup=create_kb_coustom_main_menu(message.chat.id)
    )

    await notify_someone(text, 'admin', 'changer', 'executor')
    await notify_in_group_chat(text)

    await state.finish()

    return


# ИЗМЕНЯЕМ СУЩЕСТВУЮЩУЮ СУММУ
@dp.callback_query_handler(state=Reportsstate.set_change_curr)
async def set_new_curr_finished_req(call:CallbackQuery, state:FSMContext):
    '''
    - RUB
    - USD
    - EUR
    - back_main_menu
    '''
    await call.answer()
    await call.message.delete()
    # await state.update_data(set_change_curr='+')

    data_btn = cb_change_finished_req.parse(call.data)

    if data_btn['type_btn'] == 'change_sum':
        await state.update_data(set_change_curr=data_btn['curr'])

        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        if chosen_request[3] == 'выдача в офисе' or chosen_request[3] == 'доставка' or chosen_request[3] == 'кэшин':
            await state.update_data(new_curr_sign='-')

        else:
            await state.update_data(new_curr_sign='')

        result = await call.message.answer (
            text='Введите новую сумму'
        )
        await state.update_data(message_to_delete=result.message_id)
        
        await Reportsstate.change_curr_amount.set()

        return

    else:
        await call.message.answer (
            text='Выход из меню "Отчетность". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()
        
        return


# ИЗМЕНЯЕМ СУЩЕСТВУЮЩУЮ СУММУ
@dp.message_handler(state=Reportsstate.change_curr_amount)
async def set_change_sum_return(message:Message, state:FSMContext):
    data_state = await state.get_data()
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    try:
        sum_amount = int(message.text)
        
        if sum_amount <= 0:
            raise ValueError('fuck off')
        sum_amount = str(sum_amount)
        
    except Exception as e:
        print(e)
        traceback.print_exception()

        await message.answer (
            text='Изменение заявки отменено. Формат суммы не правильный.',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        
        await state.finish()

        return

    new_curr = data_state['set_change_curr']
    new_curr_sign = data_state['new_curr_sign']
    full_new_sum = new_curr_sign + message.text
    chosen_request = data_state['chosen_request']

    if new_curr == 'rub':
        chosen_request[5] = full_new_sum
        chosen_request[12] = '0'

    if new_curr == 'usd':
        chosen_request[6] = full_new_sum
        chosen_request[13] = '0'

    if new_curr == 'eur':
        chosen_request[7] = full_new_sum
        chosen_request[14] = '0'

    chosen_request[11] = 'В обработке'
    chosen_request[15] = '0'
    chosen_request[16] = '0'
    username = message.chat.username
    chosen_request[10] = username

    old_comment = chosen_request[8]
    chosen_request[8] = old_comment + f' * возвращена в обработку с измененной суммой'

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
    request_numb = chosen_request[2]
    persone = all_emoji['персона']
    request_date = chosen_request[0]
    text = f'{request_type_emoji} #N{request_numb} от {request_date}\nвозвращена в обработку измененной суммой\n{persone} @{username}'

    await message.answer (
        text='Сумма изменена, заявка возвращена в обработку!',
        reply_markup=create_kb_coustom_main_menu(message.chat.id)
    )

    await notify_someone(text, 'admin', 'changer', 'executor')
    await notify_in_group_chat(text)

    await state.finish()

    return
