
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# storage = MemoryStorage()
# dp = Dispather(bot)
# dp = Dispather(bot, storage=storage)