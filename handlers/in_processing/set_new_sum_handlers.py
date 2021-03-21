from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot, sheet
from states import Processing
from keyboards import cb_choose_currency
from keyboards import create_kb_chosen_request
from keyboards import main_menu


# from chosen_request_menu.py / change_request
@dp.callback_query_handler(state=Processing.sum_currency_to_change)
async def set_currency_to_change(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    data_btn = cb_choose_currency.parse(call.data)
    await state.update_data(sum_currency_to_change=data_btn['curr'])
    # {'@': 'cbkbws', 'curr': 'USD', 'type_btn': 'change_curr'}

    if data_btn['type_btn'] == 'back_main_menu':
        await call.message.answer (
            f'===========\nПросмотр заявок отменен\n===========',
            reply_markup=main_menu
        )
        await state.finish()
        
        return

    data_state = await state.get_data()
    request = data_state['chosen_request']

    if data_state['sum_currency_to_change'] == 'rub':
        old_sum = request[5]
        old_sum = int(old_sum)
        old_sum = abs(old_sum)
        old_sum = str(old_sum) + ' ₽'
    if data_state['sum_currency_to_change'] == 'usd':
        old_sum = request[6]
        old_sum = int(old_sum)
        old_sum = abs(old_sum)
        old_sum = str(old_sum) + ' $'
    if data_state['sum_currency_to_change'] == 'eur':
        old_sum = request[7]
        old_sum = int(old_sum)
        old_sum = abs(old_sum)
        old_sum = str(old_sum) + ' €'


    old_comment = request[8]
    new_comment = old_comment + '; прежняя сумма: ' + old_sum + ';'
    request[8] = new_comment
    await state.update_data(chosen_request=request)


    result = await call.message.answer (
        f'Старая сумма: {old_sum}. Введите новую сумму'
    )
    await state.update_data(message_to_delete=result.message_id)
    await Processing.sum_amount_to_change.set()


@dp.message_handler(state=Processing.sum_amount_to_change)
async def set_sum_for_change(message:Message, state:FSMContext):

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
        new_sum = int(message.text)
        
    except Exception as e:
        await message.answer (
            text='Изменение заявки отменено. Формат суммы не правильный.',
            reply_markup=main_menu
        )
        await state.finish()
        print(e)
    
    await state.update_data(sum_amount_to_change=new_sum)

    data_state = await state.get_data()
    request = data_state['chosen_request']

    currency = data_state['sum_currency_to_change']

    if currency == 'rub':
        old_sum = request[5]
        old_sum = str(old_sum)
        plus_or_minus = old_sum[0]

        if plus_or_minus == '-':
            plus_or_minus = '-'

        else:
            plus_or_minus = ''
            
        request[5] = plus_or_minus + str(new_sum)

    if currency == 'usd':
        old_sum = request[6]
        old_sum = str(old_sum)
        plus_or_minus = old_sum[0]

        if plus_or_minus == '-':
            plus_or_minus = '-'

        else:
            plus_or_minus = ''

        request[6] = plus_or_minus + str(new_sum)

    if currency == 'eur':
        old_sum = request[7]
        old_sum = str(old_sum)
        plus_or_minus = old_sum[0]

        if plus_or_minus == '-':
            plus_or_minus = '-'

        else:
            plus_or_minus = ''

        request[7] = plus_or_minus + str(new_sum)

    await state.update_data(chosen_request=request)

    data_state = await state.get_data()
    request = data_state['chosen_request']

    
    id_request = request[2]
    date_request = request[0]
    operation_type_request = request[3]
    request[11] = 'В обработке'

    if not request[5] == '-': sum_RUB = request[5][1:] + ' ₽\n'
    else: sum_RUB = ''

    if not request[6] == '-': sum_USD = request[6][1:] + ' $\n'
    else: sum_USD =''

    if not request[7] == '-': sum_EUR = request[7][1:] + ' €'
    else: sum_EUR = ''

    await state.update_data(chosen_request=request)

    try:
        result = await message.answer_sticker (
        'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA'
        )
        sheet.replace_row(request)

    except Exception as e:
        print(e)
        await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)
        await message.answer_sticker (
            'CAACAgIAAxkBAAL9rGBTCImgCvHJBZ-doEYr2jkvs6UEAAIaAAPANk8TgtuwtTwGQVceBA'
        )
        await message.answer (
            text='Не удалось соединиться с гугл таблицей',
            reply_markup=main_menu
        )

        return

    await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)
    
    data_state = await state.get_data()
    request = data_state['chosen_request']

    await message.answer (
        'Сумма заявки измененна.\nЗаявка #{} от {}\nоперация: {}\n{}{}{}'.format (
            id_request, 
            date_request, 
            operation_type_request,
            sum_RUB,
            sum_USD,
            sum_EUR
        ),
        reply_markup=create_kb_chosen_request(request)
    )
    
    await Processing.chosen_request_menu.set()
    # to chosen_request_menu.py
