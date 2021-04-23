from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery

from data import sticker
from data import all_emoji
from keyboards import create_kb_coustom_main_menu
from keyboards import create_kb_confirm_box_office
from loader import dp, sheet, bot
from states import Reportsstate
from utils import notify_in_group_chat
from utils import notify_someone


@dp.callback_query_handler(state=Reportsstate.confirm_recive_box_office)
async def confirm_recive_cash_box(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(confirm_give_box_office='+')

    if call.data == 'confirm_box_office':
        data_state = await state.get_data()
        text_balance = data_state['cash_box_text']
        user = '@' + call.message.chat.username
        recive_cash_box = all_emoji['recive_cash_box']

        text_start = f'#КАССА {recive_cash_box}\n'
        text_end = f'\nКАССУ ПРИНЯЛ\n{user}'

        text = text_start + text_balance + text_end
   
        await call.message.answer (
            text=text,
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await notify_in_group_chat(text)

        await state.finish()
        
        return


    if call.data == 'raise_problem':
        result = await call.message.answer('Подробно изложите выявленные расхождения')
        await state.update_data(message_to_delete=result.message_id)

        await Reportsstate.text_problem.set()

        return


    elif call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "ОТЧЕТНОСТЬ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return


@dp.callback_query_handler(state=Reportsstate.confirm_give_box_office)
async def confirm_give_cash_box(call:CallbackQuery, state:FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(confirm_give_box_office='+')

    if call.data == 'confirm_box_office':
        data_state = await state.get_data()
        text_balance = data_state['cash_box_text']
        user = '@' + call.message.chat.username
        give_cash_box = all_emoji['give_cash_box']

        text_start = f'#КАССА {give_cash_box}\n'
        text_end = f'\nКАССУ СДАЛ\n{user}'

        text = text_start + text_balance + text_end
   
        await call.message.answer (
            text=text,
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )
        await notify_in_group_chat(text)

        await state.finish()
        
        return


    if call.data == 'raise_problem':
        result = await call.message.answer('Подробно изложите выявленные расхождения')
        await state.update_data(message_to_delete=result.message_id)

        await Reportsstate.text_problem.set()

        return


    elif call.data == 'back__main_menu':
        await call.message.answer (
            text='Выход из меню "ОТЧЕТНОСТЬ". Используйте главное меню.',
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