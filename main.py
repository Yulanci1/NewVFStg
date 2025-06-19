import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from utils.scraper import check_slots
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

last_status = {}

async def background_check():
    while True:
        logger.info("Checking slots...")
        status = check_slots()
        for city, available in status.items():
            if last_status.get(city) != available:
                last_status[city] = available
                if available:
                    await bot.send_message(CHAT_ID, f"✅ Слот доступен в городе: <b>{city}</b>")
        await asyncio.sleep(180)

@dp.message(commands=["start", "help"])
async def start(message: Message):
    await message.answer("Этот бот отслеживает наличие слотов VFS France по городам России. Используй /check для ручной проверки.")

@dp.message(commands=["check"])
async def check(message: Message):
    status = check_slots()
    reply = "\n".join([f"{city}: {'✅ Есть' if available else '❌ Нет'}" for city, available in status.items()])
    await message.answer(f"Текущий статус:\n{reply}")

async def main():
    asyncio.create_task(background_check())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
