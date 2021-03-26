from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.sqlite import Database
from utils import DataFromSheet
from utils import SmsInfoSheet

from utils import DataPermits


db = Database()
sheet = DataFromSheet()
permit = DataPermits()
smsinfo = SmsInfoSheet()

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
# dp = Dispatcher(bot)
# admins = db.select_user()
dp = Dispatcher(bot, storage=storage)