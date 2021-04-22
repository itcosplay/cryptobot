# from aiogram.dispatcher import middlewares
from loader import db


async def on_startup(dispatcher):
    import filters
    # import middlewares
    filters.setup(dp)
    # middlewares.setup(dp)   
    # print(db.select_all_users())

    from utils.notify_admins import on_startup_notify
    # Уведомляет про запуск бота
    await on_startup_notify(dispatcher)


async def on_shutdown(dispatcher):
    # Уведомляет про остановку бота

    from utils.notify_admins import on_shutdown_notify
    await on_shutdown_notify(dispatcher)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    
    executor.start_polling (
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )