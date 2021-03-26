import time

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot, smsinfo
from states import SMSstate
from data import all_emoji

from keyboards import cb_for_what_waste
from keyboards import create_kb_yes_no_note

# from enter_to_smsinfo << set_who_waste
@dp.callback_query_handler(state=SMSstate.for_what_waste)
async def set_yes_no_note(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()

    data_btn = cb_for_what_waste.parse(call.data)
    
    if data_btn['type_btn'] == 'back__main_menu':
        await call.message.answer (
            f'===========\nВыход в главное меню\n===========',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return

    await state.update_data(for_what_waste=data_btn['type_btn'])

    await call.message.answer (
        text='Добавить примечание?',
        reply_markup=create_kb_yes_no_note()
    )
    await SMSstate.yes_no_note.set()
    # ---> enter_to_smsinfo.py <---