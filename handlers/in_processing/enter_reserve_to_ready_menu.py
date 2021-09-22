from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from data import sticker
from loader import dp, bot
from states import Processing
from loader import sheet
from utils import get_data_chosen_request
from utils import notify_someone
from utils import notify_in_group_chat
from utils import updating_log
from keyboards import cb_what_sum
from keyboards import create_kb_chosen_request
from keyboards import create_kb_what_sum_correct
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_what_blue


# from chosen_request_menu
@dp.callback_query_handler(state=Processing.enter_reserve_to_ready_menu)
async def choose_currency(call:CallbackQuery, state:FSMContext):
    '''
    > скорректировать
    > подтвердить
    > вернуться к заявке
    > назад - главное меню
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(enter_reserve_to_ready_menu='+')

    data_btn = cb_what_sum.parse(call.data)

    if data_btn['type_btn'] == 'correct_sum':
        data_state = await state.get_data()
        request = data_state['chosen_request']

        await call.message.answer (
            text='Выберите одну из исходных сумм по заявке',
            reply_markup=create_kb_what_sum_correct(request)
        )
        await Processing.enter_correct_sum_to_ready_menu.set()

        return

    elif data_btn['type_btn'] == 'confirm_sum':
        data_state = await state.get_data()

        chosen_request = data_state['chosen_request']
        
        # if request with RUB than the first char will be '-'
        if chosen_request[5][0] == '-':
            chosen_request[12] = chosen_request[5]

            if chosen_request[6][0] == '-':
                chosen_request[13] = chosen_request[6]
        
            if chosen_request[7][0] == '-':
                chosen_request[14] = chosen_request[7]

            await state.update_data(chosen_request=chosen_request)
            await call.message.answer (
                text='Сколько синих?',
                reply_markup=create_kb_what_blue()
                # > без синих
                # > ввести колличество синих
                # > вернуться к заявке
                # > назад - главное меню
            )
            
            await Processing.enter_to_blue_amount_menu.set()
            # to blue_amount_handlers.py
            return
        # Проверка для синих купюр если рублевая заявка
        ###############################################

        chosen_request[11] = 'Готово к выдаче'
        user = call.message.chat.username
        chosen_request[10] = user

        if chosen_request[6][0] == '-':
            chosen_request[13] = chosen_request[6]
        
        if chosen_request[7][0] == '-':
            chosen_request[14] = chosen_request[7]

        chosen_request[16] = '0' # тут синих быть не должно

        text = get_data_chosen_request(chosen_request)

        await call.message.answer (
            text = text
        )

        chosen_request[9] = updating_log('RESERVE', user, chosen_request)

        try:
            result = await call.message.answer_sticker (
                sticker['go_to_table']
            )
            sheet.replace_row(chosen_request)

        except Exception as e:
            print(e)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)
            await call.message.answer_sticker (
                sticker['not_connection']
            )
            await call.message.answer (
                text='Не удалось соединиться с гугл таблицей',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )
            await state.finish()
            
            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        text = get_data_chosen_request(chosen_request)

        await notify_someone(text, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text)

        request_id = chosen_request[2]

        await call.message.answer (
            text=f'Заявка #N{request_id} отложена на выдачу',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return

    elif data_btn['type_btn'] == 'back_to_chosen_request':
        data_state = await state.get_data()
        current_requests = data_state['current_requests']
        chosen_request = data_state['chosen_request']
        request_id = chosen_request[2]

        for request in current_requests:

            if request_id == request[2]:
                await state.update_data(chosen_request=request)

                break

        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']
        text = get_data_chosen_request(chosen_request)

        await call.message.answer (
            text=text,
            reply_markup=create_kb_chosen_request(request)
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

    elif data_btn['type_btn'] == 'back_main_menu':

        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        
        await state.finish()

        return


    
        
        