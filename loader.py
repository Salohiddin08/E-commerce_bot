from aiogram import Bot,Dispatcher, F
from data.config import BOT_TOKEN
# Import Database Class
from utils.db_api.sqlite import Database
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
bot=Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp=Dispatcher(storage=MemoryStorage())
# Create database file
db = Database(path_to_db='data/main.db')
