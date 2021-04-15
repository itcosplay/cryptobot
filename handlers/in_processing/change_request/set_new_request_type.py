from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import all_emoji
from data import sticker
from keyboards import create_kb_chosen_request
from keyboards import create_kb_coustom_main_menu
from loader import bot, dp, sheet
from states import Processing
from utils import get_data_chosen_request
from utils import notify_in_group_chat
from utils import notify_someone


@dp.callback_query_handler(state=Processing.new_request_type)
async def set_date_from_buttons(call:CallbackQuery, state:FSMContext):
    '''
    > выдача в офисе         issuing_office
    > прием кэша             cash_recive
    > доставка               delivery
    > обмен                  exchange
    > кэшин                  cash_in
    > снятие с карт          cash_out
    > вернуться к заявке     back_to_request
    > отменить главное меню  back__main_menu
    '''
    await call.answer()
    await call.message.delete()

    if call.data == 'back_to_request':
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

    elif call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return

    elif call.data == 'issuing_office':
        new_request_type = 'выдача в офисе'
    
    elif call.data == 'cash_recive':
        new_request_type = 'прием кэша'

    elif call.data == 'delivery':
        new_request_type = 'доставка'

    elif call.data == 'exchange':
        new_request_type = 'обмен'

    elif call.data == 'cash_in':
        new_request_type = 'кэшин'
    
    elif call.data == 'cash_out':
        new_request_type = 'снятие с карт'
    
    data_state = await state.get_data()
    chosen_request = data_state['chosen_request']
    request_id = chosen_request[2]
    request_type_emoji = all_emoji[chosen_request[3]]
    persone = all_emoji['персона']
    username = call.message.chat.username

    text = f'{request_type_emoji} #N{request_id}\nизменен тип заявки\n{chosen_request[3]} 👉 {new_request_type}\n{persone} @{username}'
    chosen_request[3] = new_request_type
    chosen_request[5] = '0'
    chosen_request[6] = '0'
    chosen_request[7] = '0'
    chosen_request[10] = username
    chosen_request[11] = 'В обработке'
    chosen_request[12] = '0'
    chosen_request[13] = '0'
    chosen_request[14] = '0'
    chosen_request[16] = '0'
    
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

    await call.message.answer (
        text='Тип заявки изменен',
        reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
    )

    await notify_someone(text, 'admin', 'changer', 'executor')
    await notify_in_group_chat(text)

    await state.finish()
