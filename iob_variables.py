from datetime import datetime
from telethon.sync import TelegramClient
import os

API_ID      =   os.getenv('API_ID')
API_HASH    =   os.getenv('API_HASH')
TOKEN       =   os.getenv('IGNIS_ORDER_BOT_TOKEN')

# ignis order bot (iob)
iob = TelegramClient('bot', int(API_ID), API_HASH).start(bot_token=TOKEN)
iob_tag = "@ignis_order_bot"
