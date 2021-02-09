from aiogram import Dispatcher

from data.config import ADMIN_ID


async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(ADMIN_ID, 'Бот Запущен')

async def on_shutdown_notify(dp: Dispatcher):
    await dp.bot.send_message(ADMIN_ID, 'Бот Остановлен')
