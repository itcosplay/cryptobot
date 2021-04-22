import time

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
        pass

    elif call.data == 'weekly_report':
        pass

    elif call.data == 'monthly_report':
        pass

    elif call.data == 'finished_requests':
        pass

    elif call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "ОТЧЕТНОСТЬ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return