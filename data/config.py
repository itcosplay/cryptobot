import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

ADMIN_ID = str(os.getenv('ADMIN_ID'))

# BOT_TOKEN = '1688138526:AAFlcUBIw6jdhOOohZeQewX1ciWhKUwpnOE'

# ADMIN_ID = 59677456

# from environs import Env

# # Теперь используем вместо библиотеки python-dotenv библиотеку environs
# env = Env()
# env.read_env()


# BOT_TOKEN = env.str('BOT_TOKEN')  # Забираем значение типа str
# ADMIN_ID = env.list('ADMINS')  # Тут у нас будет список из админов
# # IP = env.str("ip")  # Тоже str, но для айпи адреса хоста