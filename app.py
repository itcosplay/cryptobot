from aiogram import executor

from loader import dp
import handlers
from utils.notify_admins import on_startup_notify, on_shutdown_notify

async def on_startup(dispatcher):
    # Уведомляет про запуск бота
    await on_startup_notify(dispatcher)

async def on_shutdown(dispatcher):
    # Уведомляет про остановку бота
    await on_shutdown_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling (
        dp, 
        on_startup=on_startup, 
        on_shutdown=on_shutdown
    )