from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from data import all_emoji
from loader import dp, bot
from states import Processing
from utils import get_data_request_short
from utils import notify_someone
from utils import notify_in_group_chat

from keyboards import cb_message_keyboard
from keyboards import create_kb_coustom_main_menu


# from enter_chosen_request_menu.py/type_btn == message_to
@dp.callback_query_handler(state=Processing.message_processing)
async def message_processing(call:CallbackQuery, state:FSMContext):
    '''
    keyboards.inline.in_processing.message_keyboards.create_kb_message_keyboard
    > принял без перерасчета   recived_without
    > до сих пор не было       nobody
    > вышел из офиса           go_out_office
    > в доставке               in_delivery
    > ожидаю подтверждения     wait_confirm
    > связался                 contacted
    > свой текст сообщения     other_text
    > назад главное меню       back__main_menu
    '''
    await call.answer()
    await call.message.delete()

    data_btn = cb_message_keyboard.parse(call.data)
    print(data_btn)

    data_state = await state.get_data()
    chosen_request = data_state['chosen_request']
    text = get_data_request_short(chosen_request)
    user = '@' + call.message.chat.username
    persone = all_emoji['персона']
    envelop = all_emoji['конверт']

    text = text + envelop

    if data_btn['type_btn'] == 'recived_without':
        text = text + 'Принята без пересчета' + '\n'
        text = text + persone + user

        await call.message.answer (
            text='сообщение отправлено!',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await notify_someone(text, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text)

        await state.finish()

        return

    if data_btn['type_btn'] == 'nobody':
        text = text + 'До сих пор не было' + '\n'
        text = text + persone + user

        await call.message.answer (
            text='сообщение отправлено!',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await notify_someone(text, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text)
        await state.finish()

        return

    if data_btn['type_btn'] == 'go_out_office':
        text = text + 'Вышел из офиса' + '\n'
        text = text + persone + user

        await call.message.answer (
            text='сообщение отправлено!',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await notify_someone(text, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text)
        await state.finish()

        return

    if data_btn['type_btn'] == 'in_delivery':
        text = text + 'В доставке' + '\n'
        text = text + persone + user

        await call.message.answer (
            text='сообщение отправлено!',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await notify_someone(text, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text)
        await state.finish()

        return

    if data_btn['type_btn'] == 'wait_confirm':
        text = text + 'Ожидаю подтверждения' + '\n'
        text = text + persone + user

        await call.message.answer (
            text='сообщение отправлено!'
        )

        await notify_someone(text, 'admin', 'changer', 'executor')
        await notify_in_group_chat(text)
        await state.finish()

        return

    if data_btn['type_btn'] == 'contacted':
        text = text + 'Cвязался с клиентом, '
        await state.update_data(other_message=text)

        result = await call.message.answer (
            text='Введите ваше сообщение'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.other_message.set()

        return

    if data_btn['type_btn'] == 'other_text':
        await state.update_data(other_message=text)

        result = await call.message.answer (
            text='Введите ваше сообщение'
        )
        await state.update_data(message_to_delete=result.message_id)
        await Processing.other_message.set()

        return

    if data_btn['type_btn'] == 'back__main_menu':

        await call.message.answer (
            text='Выход из меню "В РАБОТЕ". Используйте главное меню.',
            reply_markup=create_kb_coustom_main_menu(call.message.chat.id)
        )

        await state.finish()

        return
    

@dp.message_handler(state=Processing.other_message)
async def set_other_message(message:Message, state:FSMContext):
    data_state = await state.get_data()

    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=data_state['message_to_delete']
    )

    await bot.delete_message (
        chat_id=message.chat.id,
        message_id=message.message_id
    )

    persone = all_emoji['персона']
    user = '@' + message.chat.username
    text = data_state['other_message'] + message.text + '\n'
    text = text + persone + user

    await message.answer (
        text='Cообщение отправлено!',
        reply_markup=create_kb_coustom_main_menu(message.chat.id)
    )

    await notify_someone(text, 'admin', 'changer', 'executor')
    await notify_in_group_chat(text)
    await state.finish()

    return