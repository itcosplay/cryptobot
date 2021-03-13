# from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
# from aiogram.dispatcher import FSMContext

# from filters import isExecutor_and_higher
# from loader import dp, sheet

# from keyboards import cb_particular
# from keyboards import cb_what_sum
# from keyboards import cb_choose_curr
# from keyboards import create_kb_what_sum
# from keyboards import create_kb_choose_curr

# from states import Processing


# @dp.callback_query_handler(isExecutor_and_higher(), cb_particular.filter(type_btn='to_give'))
# async def what_sum_close(call:CallbackQuery, state:FSMContext):
#     await call.message.delete()
#     await call.message.answer('С какой суммой отложить на выдачу?', reply_markup=create_kb_what_sum())


# @dp.callback_query_handler(isExecutor_and_higher(), cb_what_sum.filter(type_btn='with_current'))
# async def with_current_sum(call:CallbackQuery, state:FSMContext):
#     await call.message.delete()
#     await call.message.answer('Нажата кнопака С ТЕКУЩЕЙ')


# @dp.callback_query_handler(isExecutor_and_higher(), cb_what_sum.filter(type_btn='with_another'))
# async def with_another_sum(call:CallbackQuery, state:FSMContext):
#     await call.message.delete()
#     choosed_request = await state.get_data()
#     choosed_request = choosed_request['choosed_request']

#     await call.message.answer (
#         'Выберите валюту для изменения',
#         reply_markup=create_kb_choose_curr (
#             choosed_request[5], # rub
#             choosed_request[6], # usd
#             choosed_request[7]  # eur
#         )
#     )
#     await Processing.currensy_for_change.set()


# @dp.callback_query_handler (
#     state=Processing.currensy_for_change
# )
# async def set_curr_for_change(call:CallbackQuery, state:FSMContext):
#     btn_data = cb_choose_curr.parse(call.data)
#     currensy = btn_data['curr']
#     await state.update_data(currensy_for_change=currensy)

#     await call.message.delete()
#     await call.message.answer(f'Меняем валюту {currensy}. Введите сумму:')
#     await Processing.sum_for_change.set()








