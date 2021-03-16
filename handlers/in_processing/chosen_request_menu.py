import datetime

from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, sheet
from states import Processing
from keyboards import cb_chosen_requests
from keyboards import create_kb_what_sum
from keyboards import create_kb_choose_currency
from keyboards import create_kb_current_requests


# from show_chosen_request
@dp.callback_query_handler(state=Processing.chosen_request_menu)
async def chosen_request_menu(call:CallbackQuery, state:FSMContext):
    data_btn = cb_chosen_requests.parse(call.data)
    
    if data_btn['type_btn'] == 'close':
        await call.answer()
        now = datetime.datetime.now()
        time_close = now.strftime("%d-%m-%Y %H:%M")

        data_state = await state.get_data()
        request = data_state['chosen_request']
        
        request[15] = time_close

        if request[12] != request[5]:
            old_comment = request[8]
            new_comment = old_comment + 'сумма RUB до закрытия ' + request[5]
            request[5] = request[12]
        
        if request[13] != request[6]:
            old_comment = request[8]
            new_comment = old_comment + 'сумма USD до закрытия ' + request[6]
            request[6] = request[13]

        if request[14] != request[7]:
            old_comment = request[8]
            new_comment = old_comment + 'сумма EUR до закрытия ' + request[7]
            request[7] = request[14]

        request[11] = 'Исполнено'
        id_request = request[2]
        
        await call.message.delete()
        await call.message.answer(f'Заявка {id_request} ИСПОЛНЕННА')

        await state.finish()
        sheet.replace_row(request)

        return

    if data_btn['type_btn'] == 'ready_to_give':
        await call.answer()
        await state.update_data(chosen_request_menu='chosen_request_menu')

        data_state = await state.get_data()
        request = data_state['chosen_request']

        await call.message.delete()
        await call.message.answer (
            'С какой суммой отложить на выдачу?',
            reply_markup=create_kb_what_sum(request)
        )
        await Processing.chosen_sum_to_ready.set()
        # to currency_and_sum_to_ready.py

        return

    if data_btn['type_btn'] == 'change':
        await call.answer()
        await state.update_data(chosen_request_menu='change_request')

        data_state = await state.get_data()
        request = data_state['chosen_request']

        await call.message.delete()
        await call.message.answer (
            'Какую сумму меняем?',
            reply_markup=create_kb_choose_currency(request)
        )
        await Processing.sum_currency_to_change.set()
        # to set_new_sum_handlers
        return

    if data_btn['type_btn'] == 'cancel':
        await call.answer()
        await state.update_data(chosen_request_menu='cancel')
        data_state = await state.get_data()
        request = data_state['chosen_request']
        request[11] = 'Отменена'
        await call.message.delete()
        await call.message.answer(
            f'Заявка {request[2]} ОТМЕНЕНА'
        )
        sheet.replace_row(request)
        await state.finish()
        
        return

    if data_btn['type_btn'] == 'back':
        try:
            current_requests,\
            in_processing_requests,\
            ready_to_give_requests = \
            sheet.get_numbs_processing_and_ready_requests()      

        except Exception as e:
            print(e)
            await call.message.answer('Не удалось получить данные с гугл таблицы :(')

            return

        await call.answer()
        await state.update_data(current_requests=current_requests)
        
        if len(in_processing_requests) == 0 and len(ready_to_give_requests) == 0:
            await call.message.answer('Все заявки исполненны.')
            await state.finish()
            
        else:
            await call.message.delete()
            await call.message.answer (
                'Текущие заявки:',
                reply_markup=create_kb_current_requests (
                    in_processing_requests,
                    ready_to_give_requests
                )
            )
            await Processing.chosen_request.set()
            # to show_chosen_requests.py

            return