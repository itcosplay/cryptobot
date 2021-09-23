import traceback

from aiogram.types import Update

from loader import dp


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler.
    Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """
    from aiogram.utils.exceptions import (
        Unauthorized,
        InvalidQueryID,
        TelegramAPIError,
        CantDemoteChatCreator,
        MessageNotModified,
        MessageToDeleteNotFound,
        MessageTextIsEmpty,
        RetryAfter,
        CantParseEntities,
        MessageCantBeDeleted,
        BadRequest
    )

    if isinstance(exception, CantDemoteChatCreator):
        print('==ERROR==\nCantDemoteChatCreator\n==ERROR==')
        print(exception)
        traceback.print_exc()

        return True

    if isinstance(exception, MessageNotModified):
        print('==ERROR==\nMessageNotModified\n==ERROR==')
        print(exception)
        traceback.print_exc()

        return True

    if isinstance(exception, MessageCantBeDeleted):
        print('==ERROR==\nMessageCantBeDeleted\n==ERROR==')
        print(exception)
        traceback.print_exc()

        return True

    if isinstance(exception, MessageToDeleteNotFound):
        print('==ERROR==\nMessageToDeleteNotFound\n==ERROR==')
        print(exception)
        traceback.print_exc()

        return True

    if isinstance(exception, MessageTextIsEmpty):
        print('==ERROR==\nMessageTextIsEmpty\n==ERROR==')
        print(exception)
        traceback.print_exc()

        return True

    if isinstance(exception, Unauthorized):
        print('==ERROR==\nUnauthorized\n==ERROR==')
        print(exception)
        traceback.print_exc()

        return True

    if isinstance(exception, InvalidQueryID):
        print('==ERROR==\nInvalidQueryID\n==ERROR==')
        print(exception)
        traceback.print_exc()

        return True

    if isinstance(exception, CantParseEntities):
        print('==ERROR==\nCantParseEntities\n==ERROR==')
        await Update.get_current().message.answer (
            f'ERROR!!!. CantParseEntities: {exception.args}'
        )
        print(exception)
        traceback.print_exc()

        return True

    if isinstance(exception, RetryAfter):
        print('==ERROR==\nRetryAfter\n==ERROR==')
        print(exception)
        traceback.print_exc()

        return True

    if isinstance(exception, BadRequest):
        print('==ERROR==\nBadRequest\n==ERROR==')
        print(exception)
        traceback.print_exc()

        return True

    if isinstance(exception, TelegramAPIError):
        print('==ERROR==\nTelegramAPIError\n==ERROR==')
        print(exception)
        traceback.print_exc()

        return True