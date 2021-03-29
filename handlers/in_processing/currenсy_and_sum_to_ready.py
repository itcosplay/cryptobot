from keyboards.inline.in_processing.keyboards_sum_ready import create_kb_choose_currency_processing
import data
from keyboards.inline import request_kb
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states import Processing
from loader import sheet
from keyboards import cb_what_sum
from keyboards import create_kb_chosen_request
from keyboards import create_kb_what_sum_correct
from keyboards import main_menu
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_what_blue


# from chosen_request_menu
# меню -с текущей- ; -корректировать- ; -вернуться к заявке- ; -назад главное меню- 
@dp.callback_query_handler(state=Processing.chosen_sum_to_ready)
async def choose_currency(call:CallbackQuery, state:FSMContext):

    data_btn = cb_what_sum.parse(call.data)

    if data_btn['type_btn'] == 'with_current':
        await call.answer()
        await call.message.delete()

        await state.update_data(chosen_sum_to_ready='with_current')

        data_state = await state.get_data()
        request = data_state['chosen_request']
        
        ###########################
        if request[5] != '0':
            await call.message.answer (
                text='Сколько синих?',
                reply_markup=create_kb_what_blue()
            )
            
            await Processing.blue_amount.set()
            # to blue_amount_handlers.py
            return
        ###########################

        request[13] = request[6]
        request[14] = request[7]
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
            reply_markup=call.message.chat.id
        )

        await state.finish()

        return

    elif data_btn['type_btn'] == 'with_another':
        await call.answer()
        await call.message.delete()

        await state.update_data(chosen_sum_to_ready='with_another')

        data_state = await state.get_data()
        request = data_state['chosen_request']

        await call.message.answer (
            'Какую сумму меняем?',
            reply_markup=create_kb_what_sum_correct(request)
        )
        await Processing.correct_curr_sum_ready.set()
        # to correct_sum_handlers_to_ready.py
        return
    
    elif data_btn['type_btn'] == 'BACK':
        await call.answer()
        await call.message.delete()

        data_state = await state.get_data()
        request = data_state['chosen_request']

        id_request = request[2]
        date_request = request[0]
        operation_type_request = request[3]

        # убираем минусы и при обмене - добавляем плюсы
        if request[3] == 'обмен':
            if not request[5] == '0':
                rub = request[5]
                rub = str(rub)
                if rub[0] == '-': rub = rub + '₽  '
                else: rub = '+' + rub + '₽  '
            else:
                rub = ''

            if not request[6] == '0':
                usd = request[6]
                usd = str(usd)
                if usd[0] == '-': usd = usd + '$  '
                else: usd = '+' + usd + '$  '
            else:
                usd = ''

            if not request[7] == '0':
                eur = request[7]
                eur = str(eur)
                if eur[0] == '-': eur = eur + '€'
                else: eur = '+' + eur + '€'
            else:
                eur = ''

        else:
            if not request[5] == '0':
                rub = request[5]
                rub = str(rub)
                if rub[0] == '-': rub = rub[1:] + '₽  '
                else: rub = rub + '₽  '
            else: rub = ''

            if not request[6] == '0':
                usd = request[6]
                usd = str(usd)
                if usd[0] == '-': usd = usd[1:] + '$  '
                else: usd = usd + '$  '
            else: usd = ''

            if not request[7] == '0':
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
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return


    
        
        