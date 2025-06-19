import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiohttp import web
from utils.scraper import check_slots
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

last_status = {}

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Бот отслеживает слоты VFS. Команда /check запускает ручную проверку.")

@dp.message_handler(commands=['check'])
async def manual_check(message: types.Message):
    status = check_slots()
    reply = "\n".join([f"{city}: {'✅ Есть' if available else '❌ Нет'}" for city, available in status.items()])
    await message.reply(f"Текущий статус:\n{reply}")

async def background_check():
    global last_status
    while True:
        logging.info("Фоновая проверка слотов...")
        status = check_slots()
        for city, available in status.items():
            if last_status.get(city) != available:
                last_status[city] = available
                if available:
                    await bot.send_message(CHAT_ID, f"✅ Слот доступен в городе: <b>{city}</b>", parse_mode="HTML")
        await asyncio.sleep(180)

async def on_startup(dp):
    asyncio.create_task(background_check())

# AIOHTTP Web Server to keep Render happy
async def handle(request):
    return web.Response(text="Bot is running!")

def run_web_app():
    app = web.Application()
    app.router.add_get("/", handle)
    web.run_app(app, port=int(os.environ.get("PORT", 10000)))

if __name__ == '__main__':
    from threading import Thread
    web_thread = Thread(target=run_web_app)
    web_thread.start()
    executor.start_polling(dp, on_startup=on_startup)