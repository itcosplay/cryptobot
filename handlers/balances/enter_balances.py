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
        result = await call.message.answer_sticker (
            sticker['go_to_table'],
            reply_markup=ReplyKeyboardRemove()
        )

        try:
            A3, E3, G3, future_requests = sheet.get_balances_with_request()

        except Exception as e:
            print(e)
            await call.message.answer_sticker (
                sticker['not_connection']
            )
            await call.message.answer (
                text='Не удалось получить данные с гугл таблицы',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )

            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

    if call.data == 'cards_balance':
        result = await call.message.answer_sticker (
            sticker['go_to_table'],
            reply_markup=ReplyKeyboardRemove()
        )

        try:
            C1A, C1T, C1D, S1V, total = sheet.get_card_balances()

        except Exception as e:
            print(e)
            await call.message.answer_sticker (
                sticker['not_connection']
            )
            await call.message.answer (
                text='Не удалось получить данные с гугл таблицы',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )

            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)
        
        text = f'Балансы на карах:\nC1A: {C1A}\nC1Т: {C1T}\nC1Д: {C1D}\nСПВ: {S1V}\n\nВсего на картах: {total}'

        await call.message.answer (
            text=text,
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return

    if call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "БАЛАНСЫ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return