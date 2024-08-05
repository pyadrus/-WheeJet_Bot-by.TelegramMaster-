import os

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from loguru import logger

load_dotenv(dotenv_path='setting/.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
logger.info(BOT_TOKEN)

bot = Bot(token=BOT_TOKEN)

storage = MemoryStorage()  # Хранилище
dp = Dispatcher(storage=storage)

ADMIN_USER_ID = 535185511

router = Router()
dp.include_router(router)
