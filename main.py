import psycopg2
from aiogram import Dispatcher
import asyncio
from routers import router
from forBOT import bot
from config import *
from db import get_connection

dp = Dispatcher()
connection = get_connection()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

asyncio.run(main())