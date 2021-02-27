from aiogram import Dispatcher

from .bloked_user import BlokedUser
from .IsAdmin import IsAdmin
from .isAdmin_or_isChanger import isAdmin_or_isChanger


def setup(dp: Dispatcher):
    dp.filters_factory.bind(BlokedUser)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(isAdmin_or_isChanger)