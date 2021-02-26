from aiogram import types

from loader import dp
from states import Request


@dp.message_handler(text='создать заявку')
async def enter_to_request(message:types.Message):
    from keyboards.inline.request_kb import create_kb_request_from

    keyboard = create_kb_request_from()
    
    await message.answer (
        'Создаем заявку! Через кого создаем заявку?',
        reply_markup = keyboard
    )
    await Request.executor.set()
