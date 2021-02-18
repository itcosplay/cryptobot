from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup (

    keyboard = [
        [
            KeyboardButton(text='права пользователей'),
            KeyboardButton(text='информация о смс')
        ],
        [
            KeyboardButton(text='создать заявку'),
            KeyboardButton(text='в работе')
        ],
        [
            KeyboardButton(text='заказать пропуск'),
            KeyboardButton(text='активные пропуска')
        ],
        [
            KeyboardButton(text='пропуска за текущие сутки'),
        ]
    ]

)