from aiogram import Bot, Dispatcher
from database.config import BOT_TOCKEN
from bot.handlers import router
from database.db_utils import create_tables

bot = Bot(token=BOT_TOCKEN)
dp = Dispatcher()


async def start_bot():
    await create_tables()

async def main():
    dp.include_router(router)
    dp.startup.register(start_bot)
    await dp.start_polling(bot, skip_updates=True)