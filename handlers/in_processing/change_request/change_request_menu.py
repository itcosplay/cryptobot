from keyboards.default.admin_keyboard import create_kb_coustom_main_menu
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from data import sticker
from data import all_emoji
from keyboards import cb_change_request
from keyboards import create_kb_change_date
from keyboards import create_kb_new_request_type
from keyboards import create_kb_which_sum_close
from keyboards import create_kb_another_currecy_add
from loader import dp, bot, sheet
from states import Processing
from utils import notify_in_group_chat
from utils import notify_someone


@dp.callback_query_handler(state=Processing.change_request_menu)
async def change_request_menu_handler(call:CallbackQuery, state:FSMContext):
    '''
    keyboards/inline/in_processin/change_request_keyboards.create_kb_change_request
    > иная дата             another_data
    > новый номер           new_id
    > переопределить тип    change_type
    > изменить сумму        update_sum
    > другая валюта         more_currency
    > добавить коментарий   add_comment
    > назад - главное меню  back__main_menu
    '''
    await call.answer()
    await call.message.delete()
    await state.update_data(change_request_menu='+')

    data_btn = cb_change_request.parse(call.data)

    if data_btn['type_btn'] == 'another_data':
        await call.message.answer (
            text='Выберите дату',
            reply_markup=create_kb_change_date()
        )
        await Processing.select_date.set()

    elif data_btn['type_btn'] == 'new_id':
        result = await call.message.answer (
            text='Введите новый четырех значный номер заявки'
        )
        
        await state.update_data(message_to_delete=result.message_id)
        await Processing.new_request_id.set()

        return

    elif data_btn['type_btn'] == 'change_type':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        await call.message.answer (
            text='Выберите новый тип заявки',
            reply_markup=create_kb_new_request_type(chosen_request[3])
        )
        await Processing.new_request_type.set()

        return

    elif data_btn['type_btn'] == 'update_sum':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        await call.message.answer (
            text='Какая сумма будет изменена?',
            reply_markup=create_kb_which_sum_close(chosen_request)
        )
        await Processing.which_sum_change.set()

        return

    elif data_btn['type_btn'] == 'more_currency':
        data_state = await state.get_data()
        chosen_request = data_state['chosen_request']

        if chosen_request[5] == '0' or chosen_request[6] == '0' or chosen_request[7] == '0':
            await call.message.answer (
                text='Выберите валюту, которую необходимо добавить?',
                reply_markup=create_kb_another_currecy_add(chosen_request)
            )
            await Processing.another_currency_add_menu.set()        
        else:
            await call.message.answer (
                text='Невозможно добавить другую валюту... Выход в главное меню',
                reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
            )
            await state.finish()

        return

    elif data_btn['type_btn'] == 'add_comment':
        await call.message.answer (
            text='Введите коментарий'
        )
        await Processing.add_another_comment.set()

        return

    elif data_btn['type_btn'] == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await state.finish()
        
        return
    

@dp.message_handler(state=Processing.add_another_comment)
async def add_another_comment(message:Message, state:FSMContext):
    data_state = await state.get_data()
    chosen_request = data_state['chosen_request']
    
    if chosen_request[8] != '0':
        comment = chosen_request[8] + ' * '

    else:
        comment = ''
    

    comment = comment + message.text
    chosen_request[8] = comment

    try:
        result = await message.answer_sticker (
            sticker['go_to_table']
        )
        sheet.replace_row(chosen_request)

    except Exception as e:
        print(e)
        await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)
        await message.answer_sticker (
            sticker['not_connection']
        )
        await message.answer (
            text='Не удалось соединиться с гугл таблицей',
            reply_markup=create_kb_coustom_main_menu(message.chat.id)
        )

        return

    await bot.delete_message(chat_id=message.chat.id, message_id=result.message_id)

    request_type_emoji = all_emoji[chosen_request[3]]
    request_id = chosen_request[2]
    persone = all_emoji['персона']
    username = message.chat.username

    text = f'{request_type_emoji} #N{request_id}\nдобавлен коментарий\n-----\n{message.text}\n{persone} {username}'

    await message.answer (
        text='Коментарий добавлен',
        reply_markup=create_kb_coustom_main_menu(message.chat.id)
    )

    await notify_someone(text, 'admin', 'changer', 'executor')
    await notify_in_group_chat(text)

    await state.finish()

    return