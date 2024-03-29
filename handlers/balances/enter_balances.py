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
from keyboards import create_kb_what_balance_to_show
from loader import dp, sheet, bot, smsinfo
from states import Balancestate
from utils import get_single_value_float
from utils import get_single_value_int
from utils import get_single_value_without_cur
from utils import get_minus_MNO


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

    await bot.delete_message (
        chat_id=message.chat.id, 
        message_id=result.message_id
    )

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
            ready_to_give_requests = sheet.get_ready_to_give_requests()

        except Exception as e:
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

        fns = all_emoji['balance_finish']
        monbag = all_emoji['money_bag']
        red_circle = all_emoji['red_circle']
        blu_circle = all_emoji['синих']
        future_money = all_emoji['future_money']
        A3 = int(A3)
        A3 = get_single_value_int(A3, 'rub')

        if A3[0] == '-': A3 = all_emoji['квз'] + A3

        E3 = int(E3)
        E3 = get_single_value_int(E3, 'usd')

        if E3[0] == '-': E3 = all_emoji['квз'] + E3

        G3 = int(G3)
        G3 = get_single_value_int(G3, 'eur')

        if G3[0] == '-': G3 = all_emoji['квз'] + G3

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
            
        
        if future_requests != 0:
            FA3 = int(FA3)
            FA3 = get_single_value_int(FA3, 'rub')

            if FA3[0] == '-': FA3 = all_emoji['квз'] + FA3

            FE3 = int(FE3)
            FE3 = get_single_value_int(FE3, 'usd')

            if FE3[0] == '-': FE3 = all_emoji['квз'] + FE3

            FG3 = int(FG3)
            FG3 = get_single_value_int(FG3, 'eur')

            if FG3[0] == '-': FG3 = all_emoji['квз'] + FG3

            text_1 = f'{fns} Баланс по исполнении всех текущих заявок на сегодня:\n{A3}\n{E3}\n{G3}\n\n'
            text_2 = f'{monbag} Баланс фактический в сейфе:\n{D3}{red_circle}{red_bal}{Q4}\n{F3}\n{I3}\n\n'
            text_3 = f'{future_money} Баланс по исполнении всех текущих заявок, включая будущие дни:\n{FA3}\n{FE3}\n{FG3}'

            text = text_1 + text_2 + text_3

        else:
            text_1 = f'{fns} Баланс по исполнении всех текущих заявок на сегодня:\n{A3}\n{E3}\n{G3}\n\n'
            text_2 = f'{monbag} Баланс фактический в сейфе:\n{D3}{red_circle}{red_bal}{Q4}\n{F3}\n{I3}\n\n'

            text = text_1 + text_2
        
        if ready_to_give_requests != False:
            ready_to_give = all_emoji['Готово к выдаче']
            text_ready_to_give = f'\n\n{ready_to_give} Отложено к выдаче:\n'

            for request in ready_to_give_requests:
                rub, usd, eur = get_minus_MNO(request)
                if usd != '' or eur != '': rub = rub + ', '
                if eur != '': usd = usd + ', '
                if rub == ', ': rub = ''
                if usd == ', ': usd = ''
        
                request_date = request[0]
                request_numb = request[2]
                request_type = all_emoji[request[3]]
                text_ready_to_give = text_ready_to_give + f'{request_date} {request_type} {request_numb}\n     {rub}{usd}{eur}\n'
        
        else:
            text_ready_to_give = '\nОтложенных к выдаче заявок нет'
            
        text = text + text_ready_to_give

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
            C1T, C1D, C1DV, total = sheet.get_card_balances()

        except Exception as e:
            print(e)
            traceback.print_exc()
            await call.message.answer_sticker (
                sticker['not_connection']
            )
            await call.message.answer (
                text='Не удалось получить данные с гугл таблицы',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )

            return

        await bot.delete_message(chat_id=call.message.chat.id, message_id=result.message_id)

        C1T = float(C1T)
        C1T = get_single_value_float(C1T, 'rub')
        C1D = float(C1D)
        C1D = get_single_value_float(C1D, 'rub')
        C1DV = float(C1DV)
        C1DV = get_single_value_float(C1DV, 'rub')

        total = float(total)
        total = get_single_value_float(total, 'rub')

        text = f'Балансы на картах:\nC1Т: {C1T}\nC1Д: {C1D}\nС1ДВ: {C1DV}\n\nВсего на картах: {total}'

        await call.message.answer (
            text=text,
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()

        return

    if call.data == 'box_offices_2_3':
        result = await call.message.answer_sticker (
            sticker['go_to_table'],
            reply_markup=ReplyKeyboardRemove()
        )
        try:
            box_office_data = smsinfo.get_box_office_data()

        except Exception as e:
            print(e)
            traceback.print_exc()

            await call.message.answer_sticker (
                sticker['not_connection']
            )
            await call.message.answer (
                text='Не удалось получить данные с гугл таблицы',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )

            return
        
        await bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=result.message_id
        )

        box_office_2_J = box_office_data[9]
        box_office_2_J = box_office_2_J.replace(',', '.')
        box_office_2_J = float(box_office_2_J)
        box_office_2_J = get_single_value_float(box_office_2_J, 'rub')

        box_office_3_P = box_office_data[15]
        box_office_3_P = box_office_3_P.replace(',', '.')
        box_office_3_P = float(box_office_3_P)
        box_office_3_P = get_single_value_float(box_office_3_P, 'rub')

        total_Q = box_office_data[16]
        total_Q = total_Q.replace(',', '.')
        total_Q = float(total_Q)
        total_Q = get_single_value_float(total_Q, 'rub')

        card_R = box_office_data[17]
        card_R = card_R.replace(',', '.')
        card_R = float(card_R)
        card_R = get_single_value_float(card_R, 'rub')

        cash_S = box_office_data[18]
        cash_S = cash_S.replace(',', '.')
        cash_S = float(cash_S)
        cash_S = get_single_value_float(cash_S, 'rub')

        text = f'Касса 2(офис): {box_office_2_J}'
        text += f'\n\nКасса 3(личные): {box_office_3_P}'
        text += f'\n\nВСЕГО: {total_Q}'
        text += f'\nКАРТА: {card_R}'
        text += f'\nНАЛ: {cash_S}'

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
