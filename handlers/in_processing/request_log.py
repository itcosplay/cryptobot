from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Processing
from utils import get_data_chosen_request

from keyboards import create_kb_chosen_request
from keyboards import create_kb_coustom_main_menu


# from enter_chosen_request_menu.py/type_btn == show_log
@dp.callback_query_handler(state=Processing.request_log)
async def log_message_handler(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    if call.data == 'back_to_request':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        text = get_data_chosen_request(chosen_request)
        
        await call.message.answer (
            text=text,
            reply_markup=create_kb_chosen_request(chosen_request)
        )

        await Processing.enter_chosen_request_menu.set()

        return

    elif call.data == 'back_to_main_menu':

        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()
        
        return

    else:
        
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()
        
        return