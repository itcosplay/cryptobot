import data
from keyboards.inline import report_keyboards
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery

from data import sticker
from data import all_emoji
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_confirm_box_office
from keyboards import cb_finished_requests
from keyboards import create_kb_change_fin_request
from keyboards import create_kb_another_currecy_add_fin
from keyboards import cb_anoter_currency_add_fin
from loader import dp, sheet, bot
from states import Reportsstate
from utils import notify_in_group_chat
from utils import notify_someone
from utils import get_data_finished_request


@dp.callback_query_handler(state=Reportsstate.return_request_menu)
async def show_finished_request(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(return_request_menu='+')

    data_btn = cb_finished_requests.parse(call.data)

    if data_btn['type_btn'] == 'exit':
        await call.message.answer (
            text='Выход из меню "ОТЧЕТНОСТЬ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()
        
        return

    data_state = await state.get_data()
    finished_requests = data_state['finished_requests']

    for request in finished_requests:

        if data_btn['id'] == request[1]:
            await state.update_data(chosen_request=request)

            break

    data_state = await state.get_data()
    request = data_state['chosen_request']
    text = get_data_finished_request(request)

    await call.message.answer (
        text=text,
        reply_markup=create_kb_change_fin_request()
    )

    await Reportsstate.change_fin_request.set()

    return


@dp.callback_query_handler(state=Reportsstate.change_fin_request)
async def change_menu_finished_req(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(change_fin_request='+')

    data_state = await state.get_data()
    chosen_request = data_state['chosen_request']

    if call.data == 'add_another_curr':
        await call.message.answer (
            text='Выберите вылюту, которую хотите добавить',
            reply_markup=create_kb_another_currecy_add_fin(chosen_request)
        )

        await Reportsstate.set_new_curr.set()

        return


    if call.data == 'change_sum':

        return


    elif call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "ОТЧЕТНОСТЬ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return


@dp.callback_query_handler(state=Reportsstate.set_new_curr)
async def change_menu_finished_req(call:CallbackQuery, state:FSMContext):
    '''
    - RUB
    - USD
    - EUR
    - back_main_menu
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(set_new_curr='+')

    data_btn = cb_anoter_currency_add_fin.parse(call.data)

    if data_btn['type_btn'] == 'add_curr':
        await state.update_data(new_curr=data_btn['curr'])

        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        if chosen_request[3] == 'выдача в офисе' or chosen_request[3] == 'доставка' or chosen_request[3] == 'кэшин':
            await state.update_data(new_curr_sign='-')

        else:
            await state.update_data(new_curr_sign='+')

        result = await call.message.answer (
            text='Введите сумму'
        )
        await state.update_data(message_to_delete=result.message_id)
        
        await Reportsstate.add_curr_amount.set()

        return

    else:
        await call.message.answer (
            text='Выход из меню "Отчетность". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return


@dp.message_handler(state=Reportsstate.text_problem)
async def send_problem_text_to_admins(message:Message, state:FSMContext):
    data_state = await state.get_data()
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    text_start = 'Ваш запрос следующего содержания:\n'
    text_problem = '*' + message.text + '*' + '\n'
    text_end = 'отправлен администратору'
    text = text_start + text_problem + text_end

    await message.answer (
        text=text,
        reply_markup=create_kb_coustom_main_menu(message.chat.id)
    )

    kvz = all_emoji['квз']
    user = message.chat.username
    text_start_admin = f'{kvz}{kvz}{kvz}{kvz}{kvz}\nУведомление о #КАССА от @{user}\n\n'
    text = text_start_admin + message.text

    await notify_someone(text, 'admin')

    await state.finish()

    return