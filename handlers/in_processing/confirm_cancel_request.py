from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import bot, dp, sheet
from states import Processing
from keyboards import main_menu
from keyboards import create_kb_chosen_request
from keyboards import cb_confirm
from utils import notify_about_cancel_request


# from chosen_request_menu (btn: cancel_request)
@dp.callback_query_handler(state=Processing.confirm_cancel_request)
async def cancel_request(call:CallbackQuery, state:FSMContext):
    data_btn = cb_confirm.parse(call.data)
    user_id = call.from_user.id
    username = call.from_user.username

    if data_btn['type_btn'] == 'CONFIRM':
        await call.answer()
        await call.message.delete()
        data_state = await state.get_data()
        request = data_state['chosen_request']
        old_comment = request[8]
        new_comment = f'{old_comment} суммы FGH до отмены: {request[5]} {request[6]} {request[7]}'
        request[8] = new_comment
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
        await notify_about_cancel_request(request, username, user_id)

        return
  
    elif data_btn['type_btn'] == 'BACK':
        await call.answer()
        await call.message.delete()
        data_state = await state.get_data()
        request = data_state['chosen_request']
        id_request = request[2]
        date_request = request[0]
        operation_type_request = request[3]

        # убираем минусы и при обмене - добавляем плюсы
        if request[3] == 'обмен':
            if not request[5] == '-':
                rub = request[5]
                rub = str(rub)
                if rub[0] == '-': rub = rub + '₽  '
                else: rub = '+' + rub + '₽  '
            else:
                rub = ''

            if not request[6] == '-':
                usd = request[6]
                usd = str(usd)
                if usd[0] == '-': usd = usd + '$  '
                else: usd = '+' + usd + '$  '
            else:
                usd = ''

            if not request[7] == '-':
                eur = request[7]
                eur = str(eur)
                if eur[0] == '-': eur = eur + '€'
                else: eur = '+' + eur + '€'
            else:
                eur = ''

        else:
            if not request[5] == '-':
                rub = request[5]
                rub = str(rub)
                if rub[0] == '-': rub = rub[1:] + '₽  '
                else: rub = rub + '₽  '
            else: rub = ''

            if not request[6] == '-':
                usd = request[6]
                usd = str(usd)
                if usd[0] == '-': usd = usd[1:] + '$  '
                else: usd = usd + '$  '
            else: usd = ''

            if not request[7] == '-':
                eur = request[7]
                eur = str(eur)
                if eur[0] == '-': eur = eur[1:] + '€'
                else: eur = eur + '€'
            else: eur = ''

        await call.message.answer (
            'Заявка #{} от {}\n{}\n{}{}{}'.format (
                id_request, 
                date_request, 
                operation_type_request,
                rub,
                usd,
                eur
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
    




