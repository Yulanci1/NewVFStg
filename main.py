import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web
from dotenv import load_dotenv
from utils.scraper import check_slots
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

last_status = {}

@dp.message(commands=["start", "help"])
async def start(message: types.Message):
    await message.answer("Этот бот отслеживает слоты VFS. Команда /check запускает ручную проверку.")

@dp.message(commands=["check"])
async def check(message: types.Message):
    status = check_slots()
    reply = "\n".join([f"{city}: {'✅ Есть' if available else '❌ Нет'}" for city, available in status.items()])
    await message.answer(f"Текущий статус:\n{reply}")

async def background_check():
    while True:
        logger.info("Фоновая проверка слотов...")
        status = check_slots()
        for city, available in status.items():
            if last_status.get(city) != available:
                last_status[city] = available
                if available:
                    await bot.send_message(CHAT_ID, f"✅ Слот доступен в городе: <b>{city}</b>")
        await asyncio.sleep(180)

async def on_startup(app):
    asyncio.create_task(dp.start_polling(bot))
    asyncio.create_task(background_check())

# Web handler
async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get("/", handle)
app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, port=int(os.getenv("PORT", 10000)))
