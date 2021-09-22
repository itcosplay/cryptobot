from utils.notify_chat import notify_in_group_chat
from utils.notify_universal import notify_someone

from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

from data import sticker
from loader import dp, bot
from states import Processing
from loader import sheet
from utils import get_data_chosen_request
from utils import updating_log
from keyboards import create_kb_coustom_main_menu
from keyboards import cb_what_bluе
from keyboards import create_kb_confirm_blue
from keyboards import cb_confirm_blue
from keyboards import create_kb_chosen_request

# from currency_and_sum_to_redy
# меню -без синих- ; -ввести кол-во синих- ; -назад главное меню- 
@dp.callback_query_handler(state=Processing.enter_blue_amount_chunk_menu)
async def blue_amount_menu(call:CallbackQuery, state:FSMContext):
    '''
    > без синих  without_blue
    > ввести колличество синих  enter_blue
    > вернуться к заявке  back_to_request
    > назад - главное меню  back_main_menu
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(enter_to_blue_amount_menu='+')

    data_btn = cb_what_bluе.parse(call.data)

    if data_btn['type_btn'] == 'without_blue':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']
        # chosen_request[12] = chosen_request[5]
        chosen_request[10] = '0'
        chosen_request[16] = '0'
        await state.update_data(chosen_request=chosen_request)

        text = get_data_chosen_request(chosen_request)

        await call.message.answer (
            text=text,
            reply_markup=create_kb_confirm_blue()
            # > подтвердить
            # > вернуться к заявке
            # > назад - главное меню
        )
        await Processing.enter_to_confirm_chunk_menu.set()

        return

    elif data_btn['type_btn'] == 'enter_blue':
        result = await call.message.answer (
            'Введите колличество синих'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.blue_amount_chunk.set()

        return
    
    elif data_btn['type_btn'] == 'back_to_request':
        data_state = await state.get_data()
        current_requests = data_state['current_requests']
        chosen_request = data_state['chosen_request']
        request_id = chosen_request[1]

        for request in current_requests:

            if request_id == request[1]:
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


@dp.message_handler(state=Processing.blue_amount_chunk)
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
        blue_amount_chunk = int(message.text)
        blue_amount_chunk = str(blue_amount_chunk)
        
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
    
    if chosen_request[5][0] == '-':
        blue_amount_chunk = '-' + blue_amount_chunk

    chosen_request[16] = blue_amount_chunk
    await state.update_data(chosen_request=chosen_request)

    text = get_data_chosen_request(chosen_request)

    await message.answer (
        text=text,
        reply_markup=create_kb_confirm_blue()
        # > подтвердить
        # > вернуться к заявке
        # > назад - главное меню
    )

    await Processing.enter_to_confirm_blue_menu_chunk.set()

    return


@dp.callback_query_handler(state=Processing.enter_to_confirm_blue_menu_chunk)
async def confirm_blue_amount(call:CallbackQuery, state:FSMContext):
    '''
    Обрабатывает кнопки из keyboards/blue_keyboard.py
    > подтвердить  confirm
    > вернуться к заявке  back_to_request
    > назад - главное меню  back_main_menu
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(enter_to_confirm_blue_menu_chunk='+')

    data_btn = cb_confirm_blue.parse(call.data)

    if data_btn['type_btn'] == 'confirm':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        user = call.message.chat.username
        chosen_request[10] = user
        chosen_request[9] = updating_log('RECIVE', user, chosen_request)
        
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
            text=f'Принято частично по заявке #N{request_id}',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

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