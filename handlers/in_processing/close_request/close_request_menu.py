from datetime import datetime

from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

from loader import dp, bot, sheet
from states import Processing
from utils import get_data_chosen_request
from utils import get_text_before_close_request
from utils import get_text_after_close_request
from utils import notify_someone
from utils import notify_in_group_chat
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_chosen_request
from keyboards import create_kb_confirm_close_request
from keyboards import create_kb_which_sum_close
from keyboards import cb_confirm_close_request

# from: chosen_request_menu
@dp.callback_query_handler(state=Processing.close_request_menu)
async def blue_amount_menu(call:CallbackQuery, state:FSMContext):
    '''
    > подтверждаю!             confirm_close
    > закрыть с другой суммой  another_sum_close
    > скорректировать синие    correct_blue
    > вернуться к заявке       back_to_request
    > назад - главное меню     back__main_menu
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(close_request_menu='+')

    data_btn = cb_confirm_close_request.parse(call.data)

    if data_btn['type_btn'] == 'confirm_close':
        data_state = await state.get_data()
        current_requests = data_state['current_requests']
        chosen_request = data_state['chosen_request']
        request_id = chosen_request[2]
        initial_com = chosen_request[8]

        for request in current_requests:

            if request_id == request[2]:
                initial_rub = request[5]
                initial_usd = request[6]
                initial_eur = request[7]

                break

        if chosen_request[5] != initial_rub:
            initial_com = initial_com + ' || ' + 'изначальная сумма RUB:' + initial_rub
        
        if chosen_request[6] != initial_usd:
            initial_com = initial_com + ' || ' + 'изначальная сумма USD:' + initial_usd

        if chosen_request[7] != initial_eur:
            initial_com = initial_com + ' || ' + 'изначальная сумма EUR:' + initial_eur

        chosen_request[8] = initial_com
        chosen_request[10] = call.message.chat.username
        chosen_request[11] = 'Исполнено'
        chosen_request[12] = chosen_request[5]
        chosen_request[13] = chosen_request[6]
        chosen_request[14] = chosen_request[7]

        time_close=datetime.today().strftime('%H:%M (%d.%m)')
        chosen_request[15] = time_close

        print(chosen_request)

        text=get_text_after_close_request(chosen_request, initial_rub, initial_usd, initial_eur)

        await call.message.answer (
            text='Заявка закрыта!',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await notify_someone(text, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text)

        await state.finish()

        return

    elif data_btn['type_btn'] == 'another_sum_close':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        await call.message.answer (
            text='Выберите сумму для корректировки',
            reply_markup=create_kb_which_sum_close(chosen_request)
            # > rub
            # > usd
            # > eur
            # > назад главное меню
        )   
        await Processing.which_sum_correct_menu.set()

        return
    
    elif data_btn['type_btn'] == 'correct_blue':
        result = await call.message.answer (
            'Введите колличество синих'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.blue_amount_close.set()

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

    elif data_btn['type_btn'] == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return


@dp.message_handler(state=Processing.blue_amount_close)
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
        chosen_request = data_state['chosen_request']
        blue_amount_close = int(message.text)
        blue_amount_close = str(blue_amount_close)
        
    except Exception as e:
        print(e)
        await message.answer (
            text='Изменение заявки отменено. Неправильный формат синих.',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )
        await state.finish()
        
        return
    
    data_state = await state.get_data()
    chosen_request = data_state['chosen_request']

    if blue_amount_close == '0':
        pass

    elif chosen_request[5][0] == '-':
        blue_amount_close = '-' + blue_amount_close

    

    chosen_request[16] = blue_amount_close
    await state.update_data(chosen_request=chosen_request)

    text = get_text_before_close_request(chosen_request)

    await message.answer (
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
