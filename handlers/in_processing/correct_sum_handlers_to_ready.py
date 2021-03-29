from emoji import emojize

from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot, sheet
from states import Processing
from keyboards import cb_wsc
from keyboards import create_kb_chosen_request
from keyboards import main_menu
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_corrected_sum
from keyboards import cb_corrected_sum
from keyboards import create_kb_what_sum_correct
from keyboards import create_kb_what_blue


# from currency_and_sum_to_ready.py / with_another
@dp.callback_query_handler(state=Processing.correct_curr_sum_ready)
async def set_currency_to_correct(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    data_btn = cb_wsc.parse(call.data)
    await state.update_data(correct_curr_sum_ready=data_btn['curr'])
    # {'@': 'cbkbws', 'curr': 'USD', 'type_btn': 'change_curr'}

    # anprix:-:back_main_menu

    data_state = await state.get_data()
    request = data_state['chosen_request']

    # if data_btn['type_btn'] == 'back_main_menu':
    #     await call.message.answer (
    #         f'===========\nПросмотр заявок отменен\n===========',
    #         reply_markup=main_menu
    #     )
    #     await state.finish()
        
    #     return

    if data_btn['curr'] == 'rub':
        old_sum = request[5]
        old_sum = int(old_sum)
        old_sum = abs(old_sum)
        old_sum = str(old_sum) + ' ₽'
    elif data_btn['curr'] == 'usd':
        old_sum = request[6]
        old_sum = int(old_sum)
        old_sum = abs(old_sum)
        old_sum = str(old_sum) + ' $'
    elif data_btn['curr'] == 'eur':
        old_sum = request[7]
        old_sum = int(old_sum)
        old_sum = abs(old_sum)
        old_sum = str(old_sum) + ' €'
    else:
        await call.message.answer (
            f'===========\nПросмотр заявок отменен\n===========',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return

    result = await call.message.answer (
        f'Корректируемая сумма к выдаче: {old_sum}. Введите новую сумму'
    )
    await state.update_data(message_to_delete=result.message_id)

    await Processing.correct_amount_sum_ready.set()


@dp.message_handler(state=Processing.correct_amount_sum_ready)
async def set_sum_to_correct(message:Message, state:FSMContext):

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
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        await state.finish()
        print(e)
    
    await state.update_data(correct_amount_sum_ready=new_sum)

    data_state = await state.get_data()
    request = data_state['chosen_request']

    currency = data_state['correct_curr_sum_ready']

    if currency == 'rub':
        old_sum = request[5]
        old_sum = str(old_sum)
        plus_or_minus = old_sum[0]

        if plus_or_minus == '-':
            plus_or_minus = '-'

        else:
            plus_or_minus = ''
            
        request[12] = plus_or_minus + str(new_sum)
        request[5] = request[12]

    if currency == 'usd':
        old_sum = request[6]
        old_sum = str(old_sum)
        plus_or_minus = old_sum[0]

        if plus_or_minus == '-':
            plus_or_minus = '-'

        else:
            plus_or_minus = ''

        request[13] = plus_or_minus + str(new_sum)
        request[6] = request[13]

    if currency == 'eur':
        old_sum = request[7]
        old_sum = str(old_sum)
        plus_or_minus = old_sum[0]

        if plus_or_minus == '-':
            plus_or_minus = '-'

        else:
            plus_or_minus = ''

        request[14] = plus_or_minus + str(new_sum)
        request[7] = request[14]

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
    operation_type_request = emo_in_chosen_request[request[3]]

    # убираем минусы и при обмене - добавляем плюсы (M,N,O)
    if request[3] == 'обмен':
        if not request[12] == '0':
            rub = request[12]
            rub = str(rub)
            if rub[0] == '-': rub = rub + '₽  '
            else: rub = '+' + rub + '₽  '
        else:
            rub = ''

        if not request[13] == '0':
            usd = request[13]
            usd = str(usd)
            if usd[0] == '-': usd = usd + '$  '
            else: usd = '+' + usd + '$  '
        else:
            usd = ''

        if not request[14] == '0':
            eur = request[14]
            eur = str(eur)
            if eur[0] == '-': eur = eur + '€'
            else: eur = '+' + eur + '€'
        else:
            eur = ''

    else:
        if not request[12] == '0':
            rub = request[12]
            rub = str(rub)
            if rub[0] == '-': rub = rub[1:] + '₽  '
            else: rub = rub + '₽  '
        else: rub = ''

        if not request[13] == '0':
            usd = request[13]
            usd = str(usd)
            if usd[0] == '-': usd = usd[1:] + '$  '
            else: usd = usd + '$  '
        else: usd = ''

        if not request[14] == '0':
            eur = request[14]
            eur = str(eur)
            if eur[0] == '-': eur = eur[1:] + '€'
            else: eur = eur + '€'
        else: eur = ''

    await state.update_data(chosen_request=request)


    await message.answer (
        text=f'#{id_request} {operation_type_request} от {date_request}\nОтложить к выдаче c суммами?\n{rub}{usd}{eur}',
        reply_markup=create_kb_corrected_sum()
    )
    
    await Processing.confirm_correct_to_ready.set()
    # to chosen_request_menu.py


@dp.callback_query_handler(state=Processing.confirm_correct_to_ready)
async def confirm_correct_to_ready(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    data_btn = cb_corrected_sum.parse(call.data)

    if data_btn['type_btn'] == 'confirm':
        data_state = await state.get_data()
        request = data_state['chosen_request']

        ###########################
        if request[5] != '-':
            await call.message.answer (
                text='Сколько синих?',
                reply_markup=create_kb_what_blue()
            )
            
            await Processing.blue_amount.set()
            # to blue_amount_handlers.py
            return
        ###########################

        request[11] = 'Готово к выдаче'
        request[16] = '0' # тут синих быть не должно

        try:
            result = await call.message.answer_sticker (
            'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA'
            )
            sheet.replace_row(request)

        except Exception as e:
            print(e)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)
            await call.message.answer_sticker (
                'CAACAgIAAxkBAAL9rGBTCImgCvHJBZ-doEYr2jkvs6UEAAIaAAPANk8TgtuwtTwGQVceBA'
            )
            await call.message.answer (
                text='Не удалось соединиться с гугл таблицей',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )

            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        data_state = await state.get_data()
        request = data_state['chosen_request']

        id_request = request[2]

        await call.message.answer (
            text=f'Заявка #{id_request} отложена к выдаче.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return

    if data_btn['type_btn'] == 'correct_else':
        data_state = await state.get_data()
        request = data_state['chosen_request']

        await call.message.answer (
            'Какую сумму меняем?',
            reply_markup=create_kb_what_sum_correct(request)
        )
        await Processing.correct_curr_sum_ready.set()
        # to def set_currency_to_correct
        return

    else: # back_main_menu
        await call.message.answer (
            text='===========\nВыход из меню "в работе". Используйте главное меню\n===========',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return
