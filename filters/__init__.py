from aiogram import Dispatcher

from .bloked_user import BlokedUser


def setup(dp: Dispatcher):
    dp.filters_factory.bind(BlokedUser)