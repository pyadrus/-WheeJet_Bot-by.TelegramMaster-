import os

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from loguru import logger

load_dotenv(dotenv_path='setting/.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
logger.info(BOT_TOKEN)
ADMIN_USER_ID = list(map(int, os.getenv('ADMIN_USER_ID').split(',')))
logger.info(ADMIN_USER_ID)

bot = Bot(token=BOT_TOKEN)

storage = MemoryStorage()  # Хранилище
dp = Dispatcher(storage=storage)

router = Router()
dp.include_router(router)
