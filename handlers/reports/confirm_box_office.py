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

        return

    elif call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "ОТЧЕТНОСТЬ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return