async def on_startup(dispatcher):
    import filters

    from utils.notify_admins import on_startup_notify

    filters.setup(dp)


    await on_startup_notify(dispatcher)


async def on_shutdown(dispatcher):
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