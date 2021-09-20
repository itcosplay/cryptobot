from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from data import all_emoji
from loader import dp, bot
from states import Processing
from utils import get_data_request_short
from utils import notify_someone
from utils import notify_in_group_chat

from keyboards import cb_message_keyboard
from keyboards import create_kb_coustom_main_menu


# from enter_chosen_request_menu.py/type_btn == show_log
@dp.callback_query_handler(state=Processing.message_processing)
async def message_processing(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    return