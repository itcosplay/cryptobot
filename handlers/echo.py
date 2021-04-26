from aiogram import types
from loader import dp, bot

from aiogram.dispatcher.filters import IDFilter


@dp.message_handler(IDFilter(chat_id='-404213737'))
async def bot_echo(message: types.Message):

    return True


@dp.message_handler()
async def bot_echo(message: types.Message):
    chat_id = message.from_user.id
    text = '''
        Используйте команду:\n
        /start
    ''' 

    await bot.send_message(chat_id=chat_id, text=text)

    return


@dp.callback_query_handler()
async def bot_echo_callback_query(call:types.CallbackQuery):
    text = '''
        Используйте команду:\n
        /start
    ''' 

    await call.message.answer(text=text)

    return




