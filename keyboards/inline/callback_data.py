from aiogram.utils.callback_data import CallbackData

group_users_data = CallbackData (
    'gud',
    'group',
    'handler'
)

change_button_data = CallbackData (
    'change_button', 
    'user_id', 
    # 'user_name',
    # 'user_status', 
    'type_button'
)

set_status_data = CallbackData (
    'set_status_button',
    'user_id',
    # 'user_name',
    # 'new_status',
    'type_button'
)