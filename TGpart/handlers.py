import datetime
from pprint import pprint
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import aiogram_calendar.dialog_calendar
import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from requests import Response
from services.ToDoServices import todo_service
from Keyboards.ClientKb import StartKb, cancel_button, show_events
from aiogram.contrib.fsm_storage import memory
from app import bot, dp, types
from states.states import CreateEvent
from aiogram_calendar import simple_cal_callback, SimpleCalendar


@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message):
    user = msg.from_user
    data = dict(username=user.username, telegram_id=user.id, full_name=user.full_name)
    res = requests.post("http://127.0.0.1:8000/users/", data=data)
    user = res.json()

    await bot.send_sticker(sticker='CAACAgIAAxkBAAEG9kFjpYem9AABYNWO9Ts1qFDXvqhTpRsAAkIQAAIzxSlJkA7UEacqSoIsBA',
                           chat_id=msg.chat.id)
    await bot.send_message(chat_id=msg.chat.id,
                           text='Выбери действие 🎲',
                           reply_markup=StartKb())
    await msg.delete()


@dp.callback_query_handler(Text(equals='Return', ignore_case=True), state='*')
async def cancel_cmd(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await callback.bot.send_message(chat_id=callback.message.chat.id,
                                    text='Выбери действие 🎲',
                                    reply_markup=StartKb())
    await callback.message.delete()


@dp.callback_query_handler(Text(equals='cancel', ignore_case=True))
async def return_cmd(callback: CallbackQuery):
    await callback.message.answer(text='Выбери действие 🎲',
                                  reply_markup=StartKb())
    await callback.message.delete()


@dp.message_handler(Text(equals='Описание', ignore_case=True))
async def desc_cmd(msg: types.Message):
    await bot.send_message(chat_id=msg.chat.id,
                           text=msg.from_user.id)
