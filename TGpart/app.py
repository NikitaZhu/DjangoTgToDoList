import requests
from aiogram import Bot, Dispatcher, executor, types
import asyncio
from config import BOT_TOKEN, admin_id
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from handlerss.events import setup as event_handler_setup
from adminpanel.admin import setup as admin_handler_setup
from handlerss.questions import setup as question_handler_setup

storage = MemoryStorage()

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)

load_dotenv()


async def sent_to_admin(dp):
    response = requests.get('http://127.0.0.1:8000/')
    try:
        if response.status_code == 200:
            await bot.send_message(chat_id=admin_id, text='Бот запущен')
    except:
        print('Сервер не запущен')


if __name__ == "__main__":
    from handlers import dp

    event_handler_setup(dp)
    admin_handler_setup(dp)
    question_handler_setup(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=sent_to_admin)
