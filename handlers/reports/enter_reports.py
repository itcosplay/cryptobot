from keyboards.inline import permits, report_keyboards
import time
import traceback

from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from data import sticker
from data import all_emoji
from filters import isExecutor_and_higher
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_reports_menu
from keyboards import create_kb_box_office
from keyboards import create_kb_what_date_report
from keyboards import create_kb_finished_requests
from loader import dp, sheet, bot
from states import Reportsstate
from utils import get_single_value_float
from utils import get_single_value_int
from utils import get_single_value_without_cur
from utils import get_minus_MNO


# from 'отчетность' main_menu
@dp.message_handler(isExecutor_and_higher(), text='отчетность')
async def show_balances_menu(message:Message, state:FSMContext):
    '''
    Обрабатывает команду "отчетность"
    '''
    await message.delete()
    
    result = await message.answer_sticker (
        sticker['balance'],
        reply_markup=ReplyKeyboardRemove()
    )

    time.sleep(0.75)
    await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)

    await message.answer (
        text='Выберите раздел',
        reply_markup=create_kb_reports_menu()
    )

    await Reportsstate.enter_the_reports.set()

    return


@dp.callback_query_handler(state=Reportsstate.enter_the_reports)
async def show_reports_menu(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(enter_the_reports='+')

    if call.data == 'box_office':
        await call.message.answer (
            text='Принять или сдать кассу?',
            reply_markup=create_kb_box_office()
        )

        await Reportsstate.recive_give_box_office.set()

        return


    elif call.data == 'daily_report':
        await call.message.answer (
            text='За какую дату смотрим отчет?',
            reply_markup=create_kb_what_date_report()
        )

        await Reportsstate.date_daily_report.set()

        return


    elif call.data == 'finished_requests':
        result = await call.message.answer_sticker (
            sticker['go_to_table']
        )

        try:
            data = sheet.get_last_30_request()
            finished_requests = []
            for row in data:
                
                if row[11] == 'Исполнено':
                    finished_requests.append(row)

            await state.update_data(finished_requests=finished_requests)

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

        await call.message.answer (
            text='Завершенные заявки:',
            reply_markup=create_kb_finished_requests(finished_requests)
        )

        await Reportsstate.return_request_menu.set()

        return


    elif call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "ОТЧЕТНОСТЬ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return