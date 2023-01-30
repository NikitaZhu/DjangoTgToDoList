from pprint import pprint

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
from config import BOT_TOKEN, admin_id
from services.ToDoServices import todo_service
import requests
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
bot = Bot(BOT_TOKEN, parse_mode="HTML")


async def tests():
    response = requests.get(url='http://127.0.0.1:8000/notifications/')
    response.raise_for_status()
    await bot.send_message(chat_id=admin_id,
                           text=f'<b>Каждый понедельник в 8 утра вам будет приходить сообщение от бота:</b>\n'
                                f'{response.json()[0]["description"]}')


async def monday(callback: CallbackQuery):
    await callback.message.answer(f'<b>Каждый понедельник в 8 утра вам будет приходить уведомление от бота</b>')
    scheduler.add_job(tests, 'cron', day_of_week='mon')
    scheduler.start()


# async def tuersday(callback: CallbackQuery):
#     scheduler.add_job(tests, trigger='cron', day_of_week='tue', hour=8)
#     scheduler.start()
#
#
# async def wednesday(callback: CallbackQuery):
#     scheduler.add_job(tests, trigger='cron', day_of_week='wed', hour=8)
#     scheduler.start()
#
#
# async def thusday(callback: CallbackQuery):
#     scheduler.add_job(tests, trigger='cron', day_of_week='thu', hour=8)
#     scheduler.start()
#
#
# async def friday(callback: CallbackQuery):
#     scheduler.add_job(tests, trigger='cron', day_of_week='fri', hour=8)
#     scheduler.start()
#
#
# async def saturday(callback: CallbackQuery):
#     scheduler.add_job(tests, trigger='cron', day_of_week='sat', hour=8)
#     scheduler.start()
#
#
# async def sunday(callback: CallbackQuery):
#     scheduler.add_job(tests, trigger='cron', day_of_week='sun', hour=8)
#     scheduler.start()


def setup(dp: Dispatcher):
    # dp.register_callback_query_handler(tests, Text(equals='mon'))
    dp.register_callback_query_handler(monday, Text(equals='monday'))
    # dp.register_callback_query_handler(tuersday, Text(equals='tuersday'))
    # dp.register_callback_query_handler(wednesday, Text(equals='wednesday'))
    # dp.register_callback_query_handler(thusday, Text(equals='thusday'))
    # dp.register_callback_query_handler(friday, Text(equals='friday'))
    # dp.register_callback_query_handler(saturday, Text(equals='saturday'))
    # dp.register_callback_query_handler(sunday, Text(equals='sunday'))
