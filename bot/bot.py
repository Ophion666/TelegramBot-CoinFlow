from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers  import start,auth, fallback, statistics, history
from handlers  import message as message_handler

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(auth.router)
dp.include_router(statistics.router)
dp.include_router(history.router)
dp.include_router(message_handler.router)
dp.include_router(fallback.router)