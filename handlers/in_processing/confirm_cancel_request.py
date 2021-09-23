from emoji import emojize

from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from data import all_emoji

from loader import bot, dp, sheet, permit
from states import Processing
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_chosen_request
from utils import get_data_chosen_request
from utils import notify_in_group_chat
from utils import notify_someone
from utils import updating_log


# from chosen_request_menu (btn: cancel_request)
@dp.callback_query_handler(state=Processing.confirm_cancel_request)
async def cancel_request(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    if call.data == 'cancel':
        username = call.message.chat.username
        data_state = await state.get_data()

        request = data_state['chosen_request']
        request[5] = '0'
        request[6] = '0'
        request[7] = '0'
        request[11] = 'Отменена'
        request[12] = '0'
        request[13] = '0'
        request[14] = '0'
        request_id = request[1]
        request[9] = updating_log('CANCEL', username, request)

        result = await call.message.answer_sticker (
            'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA'
        )

        try:
            sheet.replace_row(request)
            permit.delete_permit(request_id)

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

        request[10] = username
        request_type_emoji = all_emoji[request[3]]
        request_id = request[2]
        persone = all_emoji['персона']

        text = f'{request_type_emoji} #N{request_id}\nОТМЕНЕНА\n{persone} @{username}'

        await call.message.answer (
            f'Заявка отменена',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await notify_someone(text, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text)

        await state.finish()

        return
  
    elif call.data == 'back_to_request':
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

    else:
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return
    




