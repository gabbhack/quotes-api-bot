from aiogram import Bot, Dispatcher

from app import config
from app.api import Api


bot = Bot(config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
api = Api(config.API_HOST, config.API_KEY)
