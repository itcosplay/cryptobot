from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



group_users_buttons = InlineKeyboardMarkup (
    row_width = 1,
    inline_keyboard= [
        InlineKeyboardButton (

        )
    ]
)

group_users_buttons = InlineKeyboardMarkup(row_width=1)

groups = ['admin', 'change', 'request']

for item in groups:
    item = InlineKeyboardButton(text=item)
    group_users_buttons.insert(item)