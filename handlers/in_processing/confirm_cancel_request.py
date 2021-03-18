from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import bot, dp, sheet
from states import Processing
from keyboards import main_menu
from keyboards import create_kb_chosen_request
from keyboards import cb_confirm


# from chosen_request_menu (btn: cancel_request)
@dp.callback_query_handler(state=Processing.confirm_cancel_request)
async def cancel_request(call:CallbackQuery, state:FSMContext):
    data_btn = cb_confirm.parse(call.data)

    if data_btn['type_btn'] == 'CONFIRM':
        await call.answer()
        await call.message.delete()
        data_state = await state.get_data()
        request = data_state['chosen_request']
        old_comment = request[8]
        new_comment = f'{old_comment} суммы FGH до отмены: {request[5]} {request[6]} {request[7]}'
        request[5] = '-'
        request[6] = '-'
        request[7] = '-'
        request[11] = 'Отменена'
        request[12] = '-'
        request[13] = '-'
        request[14] = '-'

        result = await call.message.answer_sticker (
            'CAACAgIAAxkBAAL9pmBTBOfTdmX0Vi66ktpCQjUQEbHZAAIGAAPANk8Tx8qi9LJucHYeBA'
        )

        try:
            sheet.replace_row(request)

        except Exception as e:
            print(e)
            await call.message.answer_sticker (
                'CAACAgIAAxkBAAL9rGBTCImgCvHJBZ-doEYr2jkvs6UEAAIaAAPANk8TgtuwtTwGQVceBA'
            )
            await call.message.answer (
                text='Не удалось соединиться с гугл таблицей...',
                reply_markup=main_menu
            )

            return
        
        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        await call.message.answer (
            f'Заявка {request[2]} ОТМЕНЕНА',
            reply_markup=main_menu
        )
        
        await state.finish()
        
        return
  
    elif data_btn['type_btn'] == 'BACK':
        await call.answer()
        await call.message.delete()
        data_state = await state.get_data()
        request = data_state['chosen_request']
        id_request = request[2]
        date_request = request[0]
        operation_type_request = request[3]

        if not request[5] == '-': sum_RUB = request[5][1:] + ' ₽\n'
        else: sum_RUB = ''

        if not request[6] == '-': sum_USD = request[6][1:] + ' $\n'
        else: sum_USD =''

        if not request[7] == '-': sum_EUR = request[7][1:] + ' €'
        else: sum_EUR = ''

        await call.message.answer (
            '#{} от {}\n{}\n{}{}{}'.format (
                id_request, 
                date_request, 
                operation_type_request,
                sum_RUB,
                sum_USD,
                sum_EUR
            ),
            reply_markup=create_kb_chosen_request(request)
        )
        await Processing.chosen_request_menu.set()

        return

    else:
        await call.answer()
        await call.message.delete()
        await call.message.answer (
            text='===========\nВыход из меню "в работе". Используйте главное меню\n===========',
            reply_markup=main_menu
        )
        await state.finish()

        return
    




