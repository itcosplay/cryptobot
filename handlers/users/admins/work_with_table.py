from os import stat
from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from states import Request



@dp.message_handler(text='создать заявку')
async def enter_to_request(message:types.Message):
    await message.answer (
        '''
        Создаем заявку!
        Через кого создаем заявку?
        Введите "чейндж" если через чейнджа
        Введите "оператор" если через оператора
        '''
    )

    await Request.executor.set()


@dp.message_handler(state=Request.executor)
async def set_executor(message:types.Message, state:FSMContext):
    executor = message.text

    await state.update_data(executor = executor)
    await message.answer (
        '''
        Выберете тип операции.
        Введиете следущее из списка:
        - прием
        - выдача
        - доставка
        - кэшин
        - обмен
        - снятие с карт
        '''
    )
    await Request.type_of_operation.set()


@dp.message_handler(state=Request.type_of_operation)
async def set_type_of_operation(message:types.Message, state:FSMContext):
    data = await state.get_data()
    executor = data.get('executor')
    type_of_operation = message.text

    if type_of_operation == 'кэшин':
        await state.update_data(type_of_operation = type_of_operation)
        await message.answer (
            '''
            Введите с какой карты:
            - "Альфа-банк"
            - "Сбер"
            '''
        )
        await Request.type_of_card.set()
    else:
        await message.answer('Ваша заявка сформированна!')
        await message.answer (
            f'Заявка содержит следующие данные: {executor} {type_of_operation}'
        )
        await state.finish()


@dp.message_handler(state=Request.type_of_card)
async def set_type_of_card(message:types.Message, state:FSMContext):
    data = await state.get_data()
    executor = data.get('executor')
    type_of_operation = data.get('type_of_operation')
    type_of_card = message.text

    await message.answer('Ваша заявка сформированна!')
    await message.answer (
        f'Заявка содержит следующие данные: {executor} {type_of_operation} {type_of_card}'
    )
    await state.finish()