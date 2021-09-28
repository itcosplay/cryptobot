from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from data import all_emoji
from loader import dp, sheet, bot
from states import Processing
from utils import get_minus_FGH
from utils import get_text_before_close_request
from utils import get_text_message_to
from utils import get_data_chosen_request
from utils import notify_someone
from utils import notify_in_group_chat
from utils import get_data_request_unpack
from utils import updating_log
from utils import beauty_text_log_builder
from keyboards import create_kb_coustom_main_menu
from keyboards import cb_chosen_requests
from keyboards import create_kb_what_sum
from keyboards import create_kb_confirm_close_request
from keyboards import create_kb_current_requests
from keyboards import create_kb_sum_correct_chunk
from keyboards import create_kb_message_keyboard
from keyboards import create_kb_change_request
from keyboards import create_kb_confirm_cancel_request
from keyboards import create_kb_chosen_request
from keyboards import create_kb_back_button
from keyboards import create_kb_under_log


# <--- show_chosen_request.py --->
@dp.callback_query_handler(state=Processing.enter_chosen_request_menu)
async def chosen_request_menu(call:CallbackQuery, state:FSMContext):
    '''
    > отложить на выдачу (для доставки, кэшина, обмена)
    > принято частично (для приема кэша, снятия с карт, обмена)
    > закрыть заявку
    > сообщение
    > изменить заявку
    > добавить пропуск
    > добавить комментарий
    > распаковать
    > отменить заявку
    > назад
    > главное меню
    '''
    await call.answer()
    await call.message.delete()

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
        # text = get_values_MNO_or_FGH_ifMNO_is_empty(chosen_request)

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

        chosen_request = data_state['chosen_request']
        is_changed = False

        await state.update_data(changed_request=chosen_request)
        await state.update_data(is_changed=is_changed)
        await state.update_data(all_changes_data=[])

        text = get_data_chosen_request(chosen_request) + \
        '\n\n Выберите изменение:'
        
        await call.message.answer (
            text,
            reply_markup=create_kb_change_request(chosen_request, is_changed)
        )

        await Processing.change_request_menu.set()

        return

    elif data_btn['type_btn'] == 'add_permit':
        result = await call.message.answer (
            'Введите Ф.И.О. которые будут добавленны'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.add_permit.set()
        # ---> add_permit_message_handler <---

    elif data_btn['type_btn'] == 'add_comment':
        result = await call.message.answer (
            text='Напишите коментарий:',
            reply_markup=create_kb_back_button()

        )
        await state.update_data(message_to_delete=result.message_id)
        
        await Processing.add_another_comment.set()
        # ---> ./change_request/change_request_menu

        return

    elif data_btn['type_btn'] == 'unpack':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']
        username = call.message.chat.username
        chosen_request[10] = username
        chosen_request[11] = 'В обработке'
        chosen_request[12] = '0'
        chosen_request[13] = '0'
        chosen_request[14] = '0'
        chosen_request[16] = '0'
        req_id = chosen_request[1]
        chosen_request[9] = updating_log('UNPACK', username, chosen_request)

        result = await call.message.answer_sticker (
            'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA'
        )

        try:
            sheet.replace_row(chosen_request)
            current_requests,\
            in_processing_requests,\
            ready_to_give_requests =\
            sheet.get_numbs_processing_and_ready_requests()

        except Exception as e:
            print(e)
            await call.message.answer_sticker (
                'CAACAgIAAxkBAAL9rGBTCImgCvHJBZ-doEYr2jkvs6UEAAIaAAPANk8TgtuwtTwGQVceBA'
            )
            await call.message.answer (
                text='Не удалось соединиться с гугл таблицей...',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )
            await state.finish()
            
            return
        
        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)
        await state.update_data(current_requests=current_requests)

        persone = all_emoji['персона']
        text_notify_unpack = get_data_request_unpack(chosen_request)
        text_notify_unpack = text_notify_unpack + f'⚙️ Распаковано в обработку\n{persone}@{username}'

        await notify_someone(text_notify_unpack, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text_notify_unpack)

        for request in current_requests:

            if req_id == request[1]:
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

    elif data_btn['type_btn'] == 'cancel_request':
        await call.message.answer (
            text='Отменить заявку?',
            reply_markup=create_kb_confirm_cancel_request()
        )
        await Processing.confirm_cancel_request.set()
        # to confirm_cancel_requeest.py
        
        return

    elif data_btn['type_btn'] == 'show_log':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        data_log = chosen_request[9]

        if data_log == 0 or data_log == '0':
            beauty_text_log = 'лог для этой заявки отсутствует'
        else:
            beauty_text_log = beauty_text_log_builder(data_log)

        await call.message.answer (
            text=beauty_text_log,
            reply_markup=create_kb_under_log()
        )

        await Processing.request_log.set()

        return

    elif data_btn['type_btn'] == 'back':
        data_state = await state.get_data()

        in_processing_requests = data_state['in_processing_requests']        
        ready_to_give_requests = data_state['ready_to_give_requests']        

        await call.message.answer (
            'Текущие заявки:',
            reply_markup=create_kb_current_requests (
                in_processing_requests,
                ready_to_give_requests
            )
        )
        
        await Processing.chosen_request.set()

        return

    elif data_btn['type_btn'] == 'main_menu':
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return
