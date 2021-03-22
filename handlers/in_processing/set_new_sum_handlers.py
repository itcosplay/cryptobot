from emoji import emojize

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

    emo_issuing_office = emojize(':office:', use_aliases=True)    
    emo_cash_recive = emojize(':chart_with_upwards_trend:', use_aliases=True)
    emo_delivery = emojize(':steam_locomotive:', use_aliases=True)
    emo_exchange = emojize(':recycle:', use_aliases=True)
    emo_cash_in = emojize(':atm:', use_aliases=True)
    emo_cash_atm = emojize(':credit_card:', use_aliases=True)
    emo_process = emojize(':hourglass_flowing_sand:', use_aliases=True)
    emo_ready = emojize(':money_with_wings:', use_aliases=True)

    emo_in_chosen_request = {
        'выдача в офисе': emo_issuing_office,
        'прием кэша': emo_cash_recive,
        'доставка': emo_delivery,
        'обмен': emo_exchange,
        'кэшин': emo_cash_in,
        'снятие с карт': emo_cash_atm,

        'В обработке': emo_process,
        'Готово к выдаче': emo_ready
    }
    
    id_request = request[2]
    date_request = request[0]
    operation_type_request = request[3]

    request[11] = 'В обработке'
    request[16] = '-'

    # убираем минусы и при обмене - добавляем плюсы
    if request[3] == 'обмен':
        if not request[5] == '-':
            rub = request[5]
            rub = str(rub)
            if rub[0] == '-': rub = rub + '₽  '
            else: rub = '+' + rub + '₽  '
        else:
            rub = ''

        if not request[6] == '-':
            usd = request[6]
            usd = str(usd)
            if usd[0] == '-': usd = usd + '$  '
            else: usd = '+' + usd + '$  '
        else:
            usd = ''

        if not request[7] == '-':
            eur = request[7]
            eur = str(eur)
            if eur[0] == '-': eur = eur + '€'
            else: eur = '+' + eur + '€'
        else:
            eur = ''

    else:
        if not request[5] == '-':
            rub = request[5]
            rub = str(rub)
            if rub[0] == '-': rub = rub[1:] + '₽  '
            else: rub = rub + '₽  '
        else: rub = ''

        if not request[6] == '-':
            usd = request[6]
            usd = str(usd)
            if usd[0] == '-': usd = usd[1:] + '$  '
            else: usd = usd + '$  '
        else: usd = ''

        if not request[7] == '-':
            eur = request[7]
            eur = str(eur)
            if eur[0] == '-': eur = eur[1:] + '€'
            else: eur = eur + '€'
        else: eur = ''

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
        text=f'Заявка ИЗМЕНЕНА.\n#{id_request} от {date_request} {emo_in_chosen_request[operation_type_request]}\nсуммы:\n{rub}{usd}{eur}',
        reply_markup=create_kb_chosen_request(request)
    )
    
    await Processing.chosen_request_menu.set()
    # to chosen_request_menu.py
