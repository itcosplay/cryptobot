from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from filters import isExecutor_and_higher
from loader import dp, sheet
from keyboards import cb_particular
from keyboards import cb_what_sum
from keyboards import create_kb_what_sum
from states import Processing


@dp.callback_query_handler(isExecutor_and_higher(), cb_particular.filter(type_btn='to_give'))
async def what_sum_close(call:CallbackQuery, state:FSMContext):
    await call.message.delete()
    await call.message.answer('С какой суммой отложить на выдачу?', reply_markup=create_kb_what_sum())


@dp.callback_query_handler(isExecutor_and_higher(), cb_what_sum.filter(type_btn='with_current'))
async def with_current_sum(call:CallbackQuery, state:FSMContext):
    await call.message.delete()
    await call.message.answer('Нажата кнопака С ТЕКУЩЕЙ')


@dp.callback_query_handler(isExecutor_and_higher(), cb_what_sum.filter(type_btn='with_another'))
async def with_another_sum(call:CallbackQuery, state:FSMContext):
    await call.message.delete()
    choosed_request = await state.get_data()
    choosed_request = choosed_request['choosed_request']

    await call.message.answer('Выберите валюту для изменения')