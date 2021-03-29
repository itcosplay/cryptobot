from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, sheet, bot
from states import Processing
from keyboards import main_menu
from keyboards import create_kb_coustom_main_menu
from keyboards import cb_chosen_requests
from keyboards import create_kb_what_sum
from keyboards import create_kb_choose_currency_processing
from keyboards import create_kb_confirm


# <--- show_chosen_request.py --->
@dp.callback_query_handler(state=Processing.chosen_request_menu)
async def chosen_request_menu(call:CallbackQuery, state:FSMContext):
    '''
    Обрабатывает нажатие на кнопки меню:
    > отложить на выдачу
    > закрыть заявку
    > изменить заявку
    > добавить данные пропуска
    > отменить заявку
    > назад главное меню
    '''
    await call.answer()
    await call.message.delete()

    data_btn = cb_chosen_requests.parse(call.data)
    
    if data_btn['type_btn'] == 'to_ready_for_give':  
        await state.update_data(chosen_request_menu='chosen_request_menu')

        data_state = await state.get_data()
        request = data_state['chosen_request']

        await call.message.answer (
            'Откладываем на выдачу',
            reply_markup=create_kb_what_sum(request)
            # > с текущей (rub usd eur)
            # > назад главное меню
        )
        await Processing.chosen_sum_to_ready.set()
        # ---> currency_and_sum_to_ready.py <---

        return

    if data_btn['type_btn'] == 'close_request':
        # суммы в M(12),N(13),O(14) копируются в F(5),G(6),H(7)
        # если MNO!=FGH добавить в коменты ">>старые суммы перед закрытием: (F)(G)(H)<<"
        # L(11) - "Исполнено"
        # P(15) - Дата и время исполнения
        # K(10) - Исполнитель - имя исполнителя из телеги

        data_state = await state.get_data()
        request = data_state['chosen_request']

        comment = request[8]

        if not request[12] == request[5]:
            old_sum_rub = '(' + str(request[5]) + 'RUB' + ')'
            request[5] = request [12]
        else:
            old_sum_rub = ''

        if not request[13] == request[6]:
            old_sum_usd = '(' + str(request[6]) + 'USD' + ')'
            request[6] = request [13]
        else:
            old_sum_usd = ''

        if not request[14] == request[7]:
            old_sum_eur = '(' + str(request[7]) + 'EUR' + ')'
            request[7] = request [14]
        else:
            old_sum_eur = ''

        if not old_sum_rub == '' or \
            not old_sum_usd == '' or \
            not old_sum_eur == '':
            comment = comment + \
                '>>старые суммы перед закрытием: ' + \
                old_sum_rub + \
                old_sum_usd + \
                old_sum_eur + \
                '<<'
        else:
            pass

        
        request[11] = 'Исполнено'

        current_time = datetime.now().strftime("%H:%M %d-%m")
        request[15] = current_time

        name = call.from_user.username
        request[10] = name

        result = await call.message.answer_sticker (
            'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA'
        )

        try:
            sheet.replace_row(request)

        except Exception as e:
            print(e)
            await call.message.answer_sticker (
                'CAACAgIAAxkBAAL9rGBTCImgCvHJBZ-doEYr2jkvs6UEAAIaAAPANk8TgtuwtTwGQVceBA'
            )
            await call.message.answer (
                text='Не удалось соединиться с гугл таблицей...',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )

            return
        
        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        await call.message.answer (
            f'Заявка {request[2]} закрыта.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return

    if data_btn['type_btn'] == 'change_request':
      
        await state.update_data(chosen_request_menu='change_request')



        
        await call.message.answer (
            'Какую сумму меняем?',
            reply_markup=create_kb_choose_currency_processing(request)
        )
        await Processing.sum_currency_to_change.set()
        # to set_new_sum_handlers

        return

    if data_btn['type_btn'] == 'add_permit':

        await state.update_data(chosen_request_menu='add_permit')

        result = await call.message.answer (
            'Введите Ф.И.О. которые будут добавленны'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.add_permit.set()
        # ---> add_permit_message_handler <---

    if data_btn['type_btn'] == 'cancel_request':
        
        await state.update_data(chosen_request_menu='may_be_cancel')
        await call.message.answer (
            text='Подтверждаете отмену заявки?',
            reply_markup=create_kb_confirm()
        )
        await Processing.confirm_cancel_request.set()
        # to confirm_cancel_requeest.py
        
        return

    if data_btn['type_btn'] == 'back_main_menu':
        await call.message.answer (
            text='===========\nВыход из меню "в работе". Используйте главное меню\n===========',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()
        # ---> main_menu <---
