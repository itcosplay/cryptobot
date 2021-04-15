import time

from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from data import sticker
from data import all_emoji
from filters import isExecutor_and_higher
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_what_balance_to_show
from loader import dp, sheet, bot
from states import Balancestate
from utils import get_single_value_float
from utils import get_single_value_int
from utils import get_single_value_without_cur


# from 'балансы' main_menu
@dp.message_handler(isExecutor_and_higher(), text='балансы')
async def show_balances_menu(message:Message, state:FSMContext):
    '''
    Обрабатывает команду "балансы" и выводит кнопки "офис" и "карты",
    "назад - главное меню"
    '''
    await message.delete()
    
    result = await message.answer_sticker (
        sticker['balance'],
        reply_markup=ReplyKeyboardRemove()
    )

    time.sleep(0.75)

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
            A3, E3, G3, future_requests, D3, F3, I3, Q4 = sheet.get_balances_with_request()
            FA3, FE3, FG3 = sheet.get_balance_AEG3()

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

        fns = all_emoji['balance_finish']
        monbag = all_emoji['money_bag']
        red_circle = all_emoji['red_circle']
        blu_circle = all_emoji['синих']
        future_money = all_emoji['future_money']
        A3 = int(A3)
        A3 = get_single_value_int(A3, 'rub')
        E3 = int(E3)
        E3 = get_single_value_int(E3, 'usd')
        G3 = int(G3)
        G3 = get_single_value_int(G3, 'eur')
        D3 = int(D3)
        Q4 = int(Q4)
        red_bal = D3-Q4

        D3 = get_single_value_int(D3, 'rub')
        red_bal = get_single_value_without_cur(red_bal)

        F3 = int(F3)
        F3 = get_single_value_int(F3, 'usd')

        I3 = int(I3)
        I3 = get_single_value_int(I3, 'eur')

        if Q4 != 0:
            Q4 = get_single_value_without_cur(Q4)
            Q4 = f'{blu_circle}{Q4}'
        else:
            Q4 = ''
            
        
        if future_requests != 0:
            FA3 = int(FA3)
            FA3 = get_single_value_int(FA3, 'rub')

            FE3 = int(FE3)
            FE3 = get_single_value_int(FE3, 'usd')

            FG3 = int(FG3)
            FG3 = get_single_value_int(FG3, 'eur')

            text_1 = f'{fns} Баланс по исполнении всех текущих заявок на сегодня:\n{A3}\n{E3}\n{G3}\n\n'
            text_2 = f'{monbag} Баланс фактический в сейфе:\n{D3}{red_circle}{red_bal}{Q4}\n{F3}\n{I3}\n\n'
            text_3 = f'{future_money} Баланс по исполнении всех текущих заявок, включая будущие дни:\n{FA3}\n{FE3}\n{FG3}'

            text = text_1 + text_2 + text_3

        else:
            text_1 = f'{fns} Баланс по исполнении всех текущих заявок на сегодня:\n{A3}\n{E3}\n{G3}\n\n'
            text_2 = f'{monbag} Баланс фактический в сейфе:\n{D3}{red_circle}{red_bal}{Q4}\n{F3}\n{I3}\n\n'

            text = text_1 + text_2

        await call.message.answer (
            text=text,
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return

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

        C1A = float(C1A)
        C1A = get_single_value_float(C1A, 'rub')
        C1T = float(C1T)
        C1T = get_single_value_float(C1T, 'rub')
        C1D = float(C1D)
        C1D = get_single_value_float(C1D, 'rub')
        S1V = float(S1V)
        S1V = get_single_value_float(S1V, 'rub')
        total = float(total)
        total = get_single_value_float(total, 'rub')
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