import datetime

import aiogram_calendar.dialog_calendar
import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

import services.EventToDo
from Keyboards.ClientKb import StartKb, cancel_button
from aiogram.contrib.fsm_storage import memory
from app import bot, dp, types
from states.states import CreateEvent
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from services import EventToDo


@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message):
    user = msg.from_user
    data = dict(username=user.username, telegram_id=user.id, full_name=user.full_name)
    res = requests.post("http://127.0.0.1:8000/users/", data=data)
    res.json()


    await bot.send_sticker(sticker='CAACAgIAAxkBAAEG9kFjpYem9AABYNWO9Ts1qFDXvqhTpRsAAkIQAAIzxSlJkA7UEacqSoIsBA',
                           chat_id=msg.chat.id)
    await msg.answer(text='Выбери действие',
                     reply_markup=StartKb())


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='Вернуться в главное меню', ignore_case=True), state='*')
async def cancel_cmd(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await message.reply('Действие отменено', reply_markup=StartKb())
    await message.delete()


@dp.message_handler(Text(equals='Описание', ignore_case=True))
async def desc_cmd(msg: types.Message):
    await bot.send_message(chat_id=msg.chat.id,
                           text=msg.from_user.id)


@dp.message_handler(Text(equals='Создать событие'))
async def create_event_cmd(msg: types.Message):
    await CreateEvent.title.set()
    await msg.answer(text='Введите название события',
                     reply_markup=cancel_button())


@dp.message_handler(state=CreateEvent.title)
async def title_state(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = msg.text
    await CreateEvent.next()
    await msg.answer(text='Введите описание события'
                     )


@dp.message_handler(state=CreateEvent.description)
async def desc_state(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = msg.text
        await msg.answer('Выберите дату события',
                         reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter(), state=CreateEvent.description)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        a = date.strftime('%Y-%m-%d')
        await state.update_data(chose_date=a)
        data = await state.get_data()
        data['user'] = callback_query.from_user.id
        await state.finish()
        await callback_query.message.answer(text=f"Событие создано:\n"
                                                 f"Название: {data['title']}\n"
                                                 f"Описание: {data['description']}\n"
                                                 f"Дата: {data['chose_date']}",
                                            reply_markup=StartKb())

        response = requests.post(f"http://localhost:8000/events/", json=data)
        response.raise_for_status()
        return response.json()


@dp.message_handler(Text(equals='Показать уже созданные события'))
async def show_events_cmd(msg: types.Message):
    pass
