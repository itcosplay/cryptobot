from aiogram import Dispatcher

from data.config import super_admins


async def on_startup_notify(dp: Dispatcher):
    for admin in super_admins:
        await dp.bot.send_message(admin, 'Бот Запущен')
    

async def on_shutdown_notify(dp: Dispatcher):
    for admin in super_admins:
        await dp.bot.send_message(admin, 'Бот Остановлен')
    