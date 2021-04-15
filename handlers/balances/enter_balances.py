import time

from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from data import sticker
from filters import isExecutor_and_higher
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_what_balance_to_show
from loader import dp, sheet, bot
from states import Balancestate


# from 'балансы' main_menu
@dp.message_handler(isExecutor_and_higher(), text='балансы')
async def show_balances_menu(message:Message, state:FSMContext):
    '''
    Обрабатывает команду "балансы" и выводит кнопки "офис" и "карты",
    "назад - главное меню"
    '''
    await message.delete()
    
    result = await message.answer (
        text='Балансы',
        reply_markup=ReplyKeyboardRemove()
    )

    time.sleep(0.5)
    await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)

    await message.answer (
        text='Какие балансы отобразить?',
        reply_markup=create_kb_what_balance_to_show()
    )
    await Balancestate.balances_menu.set()

    return


@dp.callback_query_handler(state=Balancestate.balances_menu)
async def show_balance(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(balances_menu='+')

    if call.data == 'office_balance':
        pass

    if call.data == 'cards_balance':
        pass

    if call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "БАЛАНСЫ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return