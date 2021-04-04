async def notify_in_group_chat(text):
    from loader import dp
    from data import group_chat

    await dp.bot.send_message(group_chat, text)

    return