from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from data import sticker
from loader import dp, sheet, bot
from states import Processing
from utils import get_data_chosen_request, request_data_functions
from keyboards import cb_confirm_reserve
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_chosen_request


# from: enter_correct_sum_to_ready_menu.py
@dp.callback_query_handler(state=Processing.enter_to_confirm_reserve_menu)
async def confirm_reserve_menu_handler(call:CallbackQuery, state:FSMContext):
    '''
    Обрабатывает кнопки из keyboards/confirm_reserve_to_ready.py
    > подтвердить  confirm
    > вернуться к заявке  back_to_request
    > назад - главное меню  back_main_menu
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(enter_to_confirm_reserve_menu='+')

    data_btn = cb_confirm_reserve.parse(call.data)

    if data_btn['type_btn'] == 'confirm':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']
        chosen_request[11] = 'Готово к выдаче'

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

            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        text = get_data_chosen_request(chosen_request)

        await call.message.answer (
            text=text,
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        return

    elif data_btn['type_btn'] == 'back_to_request':
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