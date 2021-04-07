from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, sheet, bot
from states import Processing
from utils import get_minus_FGH
from utils import get_plus_FGH
from utils import get_text_before_close_request
from utils import get_text_message_to
from keyboards import main_menu
from keyboards import create_kb_coustom_main_menu
from keyboards import cb_chosen_requests
from keyboards import create_kb_what_sum
from keyboards import create_kb_choose_currency_processing
from keyboards import create_kb_confirm_close_request
from keyboards import create_kb_what_sum_correct
from keyboards import create_kb_sum_correct_chunk
from keyboards import create_kb_message_keyboard


# <--- show_chosen_request.py --->
@dp.callback_query_handler(state=Processing.enter_chosen_request_menu)
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
    await state.update_data(enter_chosen_request_menu='+')

    data_btn = cb_chosen_requests.parse(call.data)

    if data_btn['type_btn'] == 'to_ready_for_give':
        # сбрасываем имя пользователя в текущей заявке
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']
        chosen_request[10] = '0'
        await state.update_data(chosen_request=chosen_request)
        # сбрасываем имя пользователя чтобы не отображалось
        ###################################################

        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        rub, usd, eur = get_minus_FGH(chosen_request)

        if not rub == '': rub = rub + '\n'
        if not usd == '': usd = usd + '\n'

        await call.message.answer (
            text=f'Откладываем на выдачу полные суммы по заявке:\n{rub}{usd}{eur}\nили корректировать суммы?',
            reply_markup=create_kb_what_sum()
            # > скорректировать
            # > подтвердить
            # > вернуться к заявке
            # > назад - главное меню
        )
        await Processing.enter_reserve_to_ready_menu.set()

        return

    elif data_btn['type_btn'] == 'recived_chunck':
        # сбрасываем имя пользователя в текущей заявке
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']
        chosen_request[10] = '0'
        await state.update_data(chosen_request=chosen_request)
        # сбрасываем имя пользователя чтобы не отображалось
        ###################################################

        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        await call.message.answer (
            text='Какая из исходных сумм по заявке принята частично?',
            reply_markup=create_kb_sum_correct_chunk(chosen_request)
            # > rub
            # > usd
            # > eur
            # > назад - главное меню
        )
        await Processing.enter_correct_sum_chunk_menu.set()

        return

    elif data_btn['type_btn'] == 'close_request':
        # L(11) - "Исполнено"
        # P(15) - Дата и время исполнения
        # K(10) - Исполнитель - имя исполнителя из телеги
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        text = get_text_before_close_request(chosen_request)

        await call.message.answer (
            text=text,
            reply_markup=create_kb_confirm_close_request(chosen_request)
            # > подтверждаю!
            # > закрыть с другой суммой
            # > скорректировать синие
            # > вернуться к заявке
            # > назад - главное меню
        )
        await Processing.close_request_menu.set()

        return

    elif data_btn['type_btn'] == 'message_to':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        text = get_text_message_to(chosen_request)

        await call.message.answer (
            text=text,
            reply_markup=create_kb_message_keyboard()
        )
        await Processing.message_processing.set()

        return

    elif data_btn['type_btn'] == 'change_request':
        data_state = await state.get_data()
        request = data_state['chosen_request']
        
        await call.message.answer (
            'Какую сумму меняем?',
            reply_markup=create_kb_choose_currency_processing(request)
        )
        await Processing.sum_currency_to_change.set()
        # to set_new_sum_handlers

        return

    elif data_btn['type_btn'] == 'add_permit':
        result = await call.message.answer (
            'Введите Ф.И.О. которые будут добавленны'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.add_permit.set()
        # ---> add_permit_message_handler <---

    elif data_btn['type_btn'] == 'cancel_request':
        await call.message.answer (
            text='Подтверждаете отмену заявки?',
            reply_markup=create_kb_confirm()
        )
        await Processing.confirm_cancel_request.set()
        # to confirm_cancel_requeest.py
        
        return

    else:
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return
