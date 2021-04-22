import time
import traceback

from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from data import sticker
from data import all_emoji
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_confirm_box_office
from loader import dp, sheet, bot
from states import Reportsstate
from utils import get_single_value_float
from utils import get_single_value_int
from utils import get_single_value_without_cur
from utils import get_minus_MNO


@dp.callback_query_handler(state=Reportsstate.recive_give_box_office)
async def show_reports_menu(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(recive_give_box_office='+')

    if call.data == 'recive_box_office':
        result = await call.message.answer_sticker (
            sticker['go_to_table']
        )

        try:
            blu_circle = all_emoji['синих']
            red_circle = all_emoji['red_circle']

            data, A3, E3, G3, D3, F3, I3, Q4 = sheet.get_large_data()
            D3 = int(D3)
            Q4 = int(Q4)
            red_bal = D3-Q4
            D3 = get_single_value_int(D3, 'rub')

            if D3[0] == '-': D3 = all_emoji['квз'] + D3

            red_bal = get_single_value_without_cur(red_bal)
            F3 = int(F3)
            F3 = get_single_value_int(F3, 'usd')

            if F3[0] == '-': F3 = all_emoji['квз'] + F3

            I3 = int(I3)
            I3 = get_single_value_int(I3, 'eur')

            if I3[0] == '-': I3 = all_emoji['квз'] + I3

            if Q4 != 0:
                Q4 = get_single_value_without_cur(Q4)
                Q4 = f'{blu_circle}{Q4}'

            else:
                Q4 = ''
            
            text = 'Сверьте данные для ПРИНЯТИЯ кассы с фактическим наличием:\n'
            text_balance = f'{D3}{red_circle}{red_bal}{Q4}\n{F3}\n{I3}'

        except Exception as e:
            print(e)
            traceback.print_exception()

            await call.message.answer_sticker (
                sticker['not_connection']
            )
            await call.message.answer (
                text='Не удалось получить данные с гугл таблицы',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )

            await state.finish()

            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        text = text + text_balance

        await call.message.answer (
            text=text,
            reply_markup=create_kb_confirm_box_office()
        )

        await Reportsstate.confirm_recive_box_office.set()

        await state.finish()

        return

    elif call.data == 'give_box_office':
        result = await call.message.answer_sticker (
            sticker['go_to_table']
        )

        try:
            blu_circle = all_emoji['синих']
            red_circle = all_emoji['red_circle']

            data, A3, E3, G3, D3, F3, I3, Q4 = sheet.get_large_data()
            D3 = int(D3)
            Q4 = int(Q4)
            red_bal = D3-Q4
            D3 = get_single_value_int(D3, 'rub')

            if D3[0] == '-': D3 = all_emoji['квз'] + D3

            red_bal = get_single_value_without_cur(red_bal)
            F3 = int(F3)
            F3 = get_single_value_int(F3, 'usd')

            if F3[0] == '-': F3 = all_emoji['квз'] + F3

            I3 = int(I3)
            I3 = get_single_value_int(I3, 'eur')

            if I3[0] == '-': I3 = all_emoji['квз'] + I3

            if Q4 != 0:
                Q4 = get_single_value_without_cur(Q4)
                Q4 = f'{blu_circle}{Q4}'

            else:
                Q4 = ''
            
            text = 'Сверьте данные для СДАЧИ кассы с фактическим наличием:\n'
            text_balance = f'{D3}{red_circle}{red_bal}{Q4}\n{F3}\n{I3}'

        except Exception as e:
            print(e)
            traceback.print_exception()

            await call.message.answer_sticker (
                sticker['not_connection']
            )
            await call.message.answer (
                text='Не удалось получить данные с гугл таблицы',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )

            await state.finish()

            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        text = text + text_balance

        await call.message.answer (
            text=text,
            reply_markup=create_kb_confirm_box_office()
        )

        await Reportsstate.confirm_give_box_office.set()

        await state.finish()

        return

    elif call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "ОТЧЕТНОСТЬ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return