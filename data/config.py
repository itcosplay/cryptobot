# import os
# from dotenv import load_dotenv


# load_dotenv()

# BOT_TOKEN = os.getenv('BOT_TOKEN')

from bt import BOT_TOKEN
from bt import SUPER_ADMINS
from bt import GROUP_CHAT
from bt import SHEET_NAME
from bt import GOOGLE_CREDENTIALS_FILE

BOT_TOKEN = BOT_TOKEN
SHEET_NAME = SHEET_NAME
GOOGLE_CREDENTIALS_FILE = GOOGLE_CREDENTIALS_FILE

# super_admins = [
#     59677456, # itcosplay
#     # 684931753 # marcofive
# ]

super_admins = SUPER_ADMINS

# group_chat = '-1001185491120' # test chat
# group_chat = '-404213737' # real chat

group_chat = GROUP_CHAT
sms_chat = '-580332170'



# ADMIN_ID = os.getenv('ADMIN_ID')

# BOT_TOKEN = '1688138526:AAFlcUBIw6jdhOOohZeQewX1ciWhKUwpnOE'

# ADMIN_ID = 59677456

# from environs import Env

# # Теперь используем вместо библиотеки python-dotenv библиотеку environs
# env = Env()
# env.read_env()


# BOT_TOKEN = env.str('BOT_TOKEN')  # Забираем значение типа str
# ADMIN_ID = env.list('ADMINS')  # Тут у нас будет список из админов
# # IP = env.str("ip")  # Тоже str, но для айпи адреса хоста