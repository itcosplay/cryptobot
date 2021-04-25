from aiogram import Dispatcher

from .bloked_user import BlokedUser
from .IsAdmin import IsAdmin
from .isAdmin_or_isChanger import isAdmin_or_isChanger
from .isExecutor import isExecutor_and_higher
from .isAdmin_or_isSecretary import isAdmin_or_isSecretary


def setup(dp: Dispatcher):
    dp.filters_factory.bind(BlokedUser)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(isAdmin_or_isChanger)
    dp.filters_factory.bind(isExecutor_and_higher)
    dp.filters_factory.bind(isAdmin_or_isSecretary)