import aiogram
from aiogram.contrib.fsm_storage.redis import RedisStorage2, RedisStorage
from aiogram.types import ParseMode

from .config import BOT_TOKEN


bot = aiogram.Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

storage = RedisStorage2()

dp = aiogram.Dispatcher(bot, storage=storage)
