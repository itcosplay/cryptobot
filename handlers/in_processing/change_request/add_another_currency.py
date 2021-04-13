from functools import singledispatch
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from data import all_emoji
from data import sticker
from loader import dp, bot, sheet
from states import Processing
from keyboards import cb_anoter_currency_add
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_confirm_close_request
from keyboards import create_kb_choose_give_recive_change
from utils import get_single_value
from utils import get_values_FGH
from utils import notify_in_group_chat
from utils import notify_someone


# from: close_request_menu.pu
@dp.callback_query_handler(state=Processing.another_currency_add_menu)
async def set_currency_to_add(call:CallbackQuery, state:FSMContext):
    '''
    - RUB
    - USD
    - EUR
    - back_main_menu
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(another_currency_add_menu='+')

    data_btn = cb_anoter_currency_add.parse(call.data)

    if data_btn['type_btn'] == 'add_curr':
        await state.update_data(another_currecy__currency=data_btn['curr'])

        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        if chosen_request[3] == 'обмен':
            await call.message.answer (
                text='Операция обмена. Сумма должна быть принята или выданна?',
                reply_markup=create_kb_choose_give_recive_change()
            )

            await Processing.another_currency__give_recive.set()

            return
        
        else:

            if chosen_request[3] == 'выдача в офисе' or chosen_request[3] == 'доставка' or chosen_request[3] == 'кэшин':
                await state.update_data(another_currency__give_recive='-')

            else:
                await state.update_data(another_currency__give_recive='+')

        result = await call.message.answer (
            text='Введите сумму'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.another_currecy__amount.set()

    else:
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return


@dp.callback_query_handler(state=Processing.another_currency__give_recive)
async def set_give_recive_to_add(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    if call.data == 'give_money':
        await state.update_data(another_currency__give_recive='-')

        result = await call.message.answer (
            text='Введите сумму'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.another_currecy__amount.set()

    elif call.data == 'recive_money':
        await state.update_data(another_currency__give_recive='+')

        result = await call.message.answer (
            text='Введите сумму'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.another_currecy__amount.set()

    else:
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return


@dp.message_handler(state=Processing.another_currecy__amount)
async def set_sum_to_add(message:Message, state:FSMContext):
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
        another_currecy__amount = int(message.text)
        
        if another_currecy__amount <= 0:
            raise ValueError('fuck off')
        another_currecy__amount = str(another_currecy__amount)
        
    except Exception as e:
        await message.answer (
            text='Изменение заявки отменено. Формат суммы не правильный.',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        await state.finish()
        print(e)

        return
    
    await state.update_data(another_currecy__amount=another_currecy__amount)
    # another_currecy__currency another_currecy__amount

    data_state = await state.get_data()
    chosen_request = data_state['chosen_request']

    currency = data_state['another_currecy__currency']
    sum = data_state['another_currecy__amount']
    sign = data_state['another_currency__give_recive']
    print('SIGN ', sign)
    if sign == '+': sign = ''
    
    if currency == 'rub':
        chosen_request[5] = sign + sum
        new_sum = get_single_value(chosen_request[5], 'rub')

    if currency == 'usd':
        print('SIGN: ', sign)
        chosen_request[6] = sign + sum
        new_sum = get_single_value(chosen_request[6], 'usd')

    if currency == 'eur':
        chosen_request[6] = sign + sum
        new_sum = get_single_value(chosen_request[6], 'eur')

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

        return

    await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)

    text = f'{request_type_emoji} #N{request_id}\nдобавлена новая сумма\n{new_sum}\n{persone} @{username}'

    await message.answer (
        text='Сумма заявки изменена',
        reply_markup=create_kb_coustom_main_menu(message.chat.id)
    )

    await notify_someone(text, 'admin', 'changer', 'executor')
    await notify_in_group_chat(text)

    await state.finish()

    return