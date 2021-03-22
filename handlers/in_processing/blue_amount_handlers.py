from emoji import emojize

from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Processing
from loader import sheet
from keyboards import create_kb_what_blue
from keyboards import main_menu
from keyboards import cb_what_bluе
from keyboards import create_kb_confirm_blue
from keyboards import cb_confirm_blue
from keyboards import create_kb_chosen_request

# from currency_and_sum_to_redy
# меню -без синих- ; -ввести кол-во синих- ; -назад главное меню- 
@dp.callback_query_handler(state=Processing.blue_amount)
async def choose_currency(call:CallbackQuery, state:FSMContext):

    data_btn = cb_what_bluе.parse(call.data)

    if data_btn['type_btn'] == 'without_blue':
        await call.answer()
        await call.message.delete()

        await state.update_data(blue_amount='without_blue')

        data_state = await state.get_data()
        request = data_state['chosen_request']

        request[12] = request[5]
        request[13] = request[6]
        request[14] = request[7]
        request[11] = 'Готово к выдаче'
        request[16] = '-'

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
                reply_markup=main_menu
            )

            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        data_state = await state.get_data()
        request = data_state['chosen_request']

        id_request = request[2]

        await call.message.answer (
            text=f'Заявка #{id_request} отложена к выдаче.',
            reply_markup=main_menu
        )

        await state.finish()

        return

    elif data_btn['type_btn'] == 'enter_blue':
        await call.answer()
        await call.message.delete()

        await state.update_data(blue_amount='enter_blue')

        data_state = await state.get_data()
        request = data_state['chosen_request']

        result = await call.message.answer (
            'Введите колличество синих?'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.enter_blue_amount.set()

        return
    
    elif data_btn['type_btn'] == 'back_to_request':
        await call.answer()
        await call.message.delete()

        data_state = await state.get_data()
        request = data_state['chosen_request']

        id_request = request[2]
        date_request = request[0]
        operation_type_request = request[3]

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

        await call.message.answer (
            'Заявка #{} от {}\n{}\n{}{}{}'.format (
                id_request, 
                date_request, 
                operation_type_request,
                rub,
                usd,
                eur
            ),
            reply_markup=create_kb_chosen_request(request)
        )

        await Processing.chosen_request_menu.set()

        return

    else: # type_btn = back_main_menu
        await call.answer()
        await call.message.delete()
        await call.message.answer (
            text='===========\nВыход из меню "в работе". Используйте главное меню\n===========',
            reply_markup=main_menu
        )
        await state.finish()

        return


@dp.message_handler(state=Processing.enter_blue_amount)
async def set_blue_amount(message:Message, state:FSMContext):

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
        enter_blue_amount = int(message.text)
        
    except Exception as e:
        await message.answer (
            text='Изменение заявки отменено. Неправильный формат синих.',
            reply_markup=main_menu
        )
        await state.finish()
        print(e)
    
    data_state = await state.get_data()
    request = data_state['chosen_request']

    if request[5][0] == '-':
        enter_blue_amount = str(enter_blue_amount)
        enter_blue_amount = '-' + enter_blue_amount

    await state.update_data(enter_blue_amount=enter_blue_amount)

    data_state = await state.get_data()
    request = data_state['chosen_request']

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

    id_request = request[2]
    # date_request = request[0]
    operation_type_request = request[3]
    enter_blue_amount = enter_blue_amount

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

    await message.answer (
        text=f'По заявке #{id_request}{emo_in_chosen_request[operation_type_request]} отложить к выдаче с суммами:\n{rub}(синими: {enter_blue_amount}){usd}{eur}',
        reply_markup=create_kb_confirm_blue()
    )
    
    await Processing.confirm_blue_amount.set()
    # to chosen_request_menu.py


@dp.callback_query_handler(state=Processing.confirm_blue_amount)
async def confirm_blue_amount(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    await state.update_data(confirm_blue_amount='confirm')

    data_btn = cb_confirm_blue.parse(call.data)

    if data_btn['type_btn'] == 'confirm':
        data_state = await state.get_data()
        request = data_state['chosen_request']

        request[16] = str(data_state['enter_blue_amount'])
        request[12] = request[5]
        request[13] = request[6]
        request[14] = request[7]
        request[11] = 'Готово к выдаче'

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
                reply_markup=main_menu
            )

            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        data_state = await state.get_data()
        request = data_state['chosen_request']

        id_request = request[2]

        await call.message.answer (
            text=f'Заявка #{id_request} отложена к выдаче.',
            reply_markup=main_menu
        )

        await state.finish()

        return

    if data_btn['type_btn'] == 'back_to_request':
        data_state = await state.get_data()
        request = data_state['chosen_request']
        
        id_request = request[2]
        date_request = request[0]
        operation_type_request = request[3]

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

        await call.message.answer (
            'Заявка #{} от {}\n{}\n{}{}{}'.format (
                id_request, 
                date_request, 
                operation_type_request,
                rub,
                usd,
                eur
            ),
            reply_markup=create_kb_chosen_request(request)
        )
        await Processing.chosen_request_menu.set()

        return
    
    else: # type_btn = back_main_menu
        await call.message.answer (
            text='===========\nВыход из меню "в работе". Используйте главное меню\n===========',
            reply_markup=main_menu
        )
        await state.finish()

        return


