from aiogram import Bot

from config import Config, load_config
from tables.sqlite import Database

config = load_config()
bot: Bot = Bot(token=config.tg_bot.token)

db  = Database()

