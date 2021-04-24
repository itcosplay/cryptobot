from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from data import all_emoji
from data import sticker
from loader import dp, bot, sheet
from states import Processing
from keyboards import cb_which_sum_close
from keyboards import create_kb_coustom_main_menu
from utils import get_single_value
from utils import get_values_FGH
from utils import notify_in_group_chat
from utils import notify_someone
from utils import notify_about_balance


# from: close_request_menu.pu
@dp.callback_query_handler(state=Processing.which_sum_change)
async def set_currency_to_correct(call:CallbackQuery, state:FSMContext):
    '''
    Обрабатывает клавиатуру create_kb_which_sum_close(request)
    - sum rub
    - sum usd
    - sum eur
    - back_main_menu
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(which_sum_change='+')

    data_btn = cb_which_sum_close.parse(call.data)

    if data_btn['type_btn'] == 'change_curr':
        await state.update_data(which_sum_change__currency=data_btn['curr'])

        result = await call.message.answer (
            text='Введите новую сумму?'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.which_sum_change__amount.set()

    else:
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return


@dp.message_handler(state=Processing.which_sum_change__amount)
async def close__sum_set(message:Message, state:FSMContext):
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
        which_sum_change__amount = int(message.text)
        
        if which_sum_change__amount < 0:
            raise ValueError('fuck off')
        which_sum_change__amount = str(which_sum_change__amount)
        
    except Exception as e:
        await message.answer (
            text='Изменение заявки отменено. Формат суммы не правильный.',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        await state.finish()
        print(e)

        return
    
    await state.update_data(which_sum_change__amount=which_sum_change__amount)
    # close__sum close__currency

    data_state = await state.get_data()
    chosen_request = data_state['chosen_request']

    correct_currency = data_state['which_sum_change__currency']
    correct_sum = data_state['which_sum_change__amount']
    
    old_rub, old_usd, old_eur = get_values_FGH(chosen_request)

    if correct_currency == 'rub':
        old_sum = old_rub

        if chosen_request[5][0] == '-':
            chosen_request[5] = str(0 - int(correct_sum))
        else: chosen_request[5] = correct_sum

        new_sum = get_single_value(chosen_request[5], 'rub')

    if correct_currency == 'usd':
        old_sum = old_usd

        if chosen_request[6][0] == '-':
            chosen_request[6] = str(0 - int(correct_sum))
        else: chosen_request[6] = correct_sum

        new_sum = get_single_value(chosen_request[6], 'usd')

    if correct_currency == 'eur':
        old_sum = old_eur

        if chosen_request[7][0] == '-':
            chosen_request[7] = str(0 - int(correct_sum))
        else: chosen_request[7] = correct_sum

        new_sum = get_single_value(chosen_request[7], 'eur')

    username = message.chat.username
    chosen_request[10] = username
    chosen_request[11] = 'В обработке'
    chosen_request[12] = '0'
    chosen_request[13] = '0'
    chosen_request[14] = '0'
    chosen_request[16] = '0'
    request_type_emoji = all_emoji[chosen_request[3]]
    request_id = chosen_request[2]
    persone = all_emoji['персона']

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

    text = f'{request_type_emoji} #N{request_id}\nизменена сумма заявки\n{old_sum} 👉 {new_sum}\n{persone} @{username}'

    await message.answer (
        text='Сумма заявки изменена',
        reply_markup=create_kb_coustom_main_menu(message.chat.id)
    )

    await notify_someone(text, 'admin', 'changer', 'executor')
    await notify_in_group_chat(text)
    await notify_about_balance()

    await state.finish()

    return