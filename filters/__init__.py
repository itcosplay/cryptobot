from aiogram import Dispatcher

from .bloked_user import BlokedUser
from .IsAdmin import IsAdmin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(BlokedUser)
    dp.filters_factory.bind(IsAdmin)