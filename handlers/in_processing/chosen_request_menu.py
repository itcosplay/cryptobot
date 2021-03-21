import datetime

from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, sheet
from states import Processing
from keyboards import cb_chosen_requests
from keyboards import create_kb_what_sum
from keyboards import create_kb_choose_currency_processing
from keyboards import create_kb_current_requests
from keyboards import main_menu
from keyboards import create_kb_confirm


# from show_chosen_request
@dp.callback_query_handler(state=Processing.chosen_request_menu)
async def chosen_request_menu(call:CallbackQuery, state:FSMContext):
    data_btn = cb_chosen_requests.parse(call.data)
    
    # if data_btn['type_btn'] == 'close':
    #     await call.answer()
    #     now = datetime.datetime.now()
    #     time_close = now.strftime("%d-%m-%Y %H:%M")

    #     data_state = await state.get_data()
    #     request = data_state['chosen_request']
        
    #     request[15] = time_close

    #     if request[12] != request[5]:
    #         old_comment = request[8]
    #         new_comment = old_comment + 'сумма RUB до закрытия ' + request[5]
    #         request[5] = request[12]
        
    #     if request[13] != request[6]:
    #         old_comment = request[8]
    #         new_comment = old_comment + 'сумма USD до закрытия ' + request[6]
    #         request[6] = request[13]

    #     if request[14] != request[7]:
    #         old_comment = request[8]
    #         new_comment = old_comment + 'сумма EUR до закрытия ' + request[7]
    #         request[7] = request[14]

    #     request[11] = 'Исполнено'
    #     id_request = request[2]
        
    #     await call.message.delete()
    #     await call.message.answer(f'Заявка {id_request} ИСПОЛНЕННА')

    #     await state.finish()
    #     sheet.replace_row(request)

    #     return

    if data_btn['type_btn'] == 'to_ready_for_give':
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

    if data_btn['type_btn'] == 'change_request':
        await call.answer()
        await state.update_data(chosen_request_menu='change_request')

        data_state = await state.get_data()
        request = data_state['chosen_request']

        await call.message.delete()
        await call.message.answer (
            'Какую сумму меняем?',
            reply_markup=create_kb_choose_currency_processing(request)
        )
        await Processing.sum_currency_to_change.set()
        # to set_new_sum_handlers
        return

    if data_btn['type_btn'] == 'cancel_request':
        await call.answer()
        await call.message.delete()
        await state.update_data(chosen_request_menu='may_be_cancel')
        await call.message.answer (
            text='Подтверждаете отмену заявки?',
            reply_markup=create_kb_confirm()
        )
        await Processing.confirm_cancel_request.set()
        # to confirm_cancel_requeest.py


        # data_state = await state.get_data()
        # request = data_state['chosen_request']
        # old_comment = request[8]
        # old_comment = f'{old_comment} суммы FGH до отмены: {request[5]} {request[6]} {request[7]}'
        # request[5] = '-'
        # request[6] = '-'
        # request[7] = '-'
        # request[11] = 'Отменена'
        # request[12] = '-'
        # request[13] = '-'
        # request[14] = '-'

        # sheet.replace_row(request)

        # await call.message.answer(
        #     f'Заявка {request[2]} ОТМЕНЕНА'
        # )
        
        # await state.finish()
        
        return

    if data_btn['type_btn'] == 'back_main_menu':
        await call.answer()
        await call.message.delete()
        await call.message.answer (
            text='===========\nВыход из меню "в работе". Используйте главное меню\n===========',
            reply_markup=main_menu
        )
        await state.finish()
