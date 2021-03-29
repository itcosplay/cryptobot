from datetime import datetime

from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext

from utils import notify_about_permit_to_order
from loader import dp, bot, permit
from states import Permitstate
from data import all_emoji
from keyboards import create_kb_coustom_main_menu


# from 'создать пропуск' main_menu
@dp.message_handler(text='создать пропуск')
async def enter_to_single_permit(message:Message, state:FSMContext):
    '''
    Запрашивает данные для отдельного пропуска
    '''
    await message.delete()
    await state.finish()
    result = await message.answer(text='Введите Ф.И.О. для пропуска')
    await state.update_data(message_to_delete=result.message_id)
    await Permitstate.single_permit_data.set()


@dp.message_handler(state=Permitstate.single_permit_data)
async def set_single_permit(message:Message, state:FSMContext):
    '''
    Создаем новый пропуск
    '''
    data_state = await state.get_data()
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )
    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    all_permit_id_list = permit.get_all_permit_id()

    permit_id = 9999
    limit_while = 1

    while True:
        if str(permit_id) in all_permit_id_list:
            permit_id -= 1
            limit_while += 1

        else:

            break

        if limit_while == 50:

            return False

    permit_id = str(permit_id)
    permit_id = permit_id.zfill(4)

    permit_text = message.text

    permit_date = datetime.today().strftime('%d.%m')

    permit.write_new_permit(permit_id, permit_date, permit_text=permit_text)
    await notify_about_permit_to_order()

    await message.answer (
        text=f'Новый пропуск #N{permit_id} добавлен, секретарь оповещен!',
        reply_markup=create_kb_coustom_main_menu(message.from_user.id)
    )

    await state.finish()