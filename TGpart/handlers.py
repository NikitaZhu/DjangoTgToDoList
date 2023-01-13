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
from states.states import CreateEvent, EventState
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
                                    text='Действие отменено',
                                    reply_markup=StartKb())
    await callback.message.delete()


@dp.message_handler(Text(equals='Описание', ignore_case=True))
async def desc_cmd(msg: types.Message):
    await bot.send_message(chat_id=msg.chat.id,
                           text=msg.from_user.id)

# @dp.message_handler(Text(equals='Создать событие'))
# async def create_event_cmd(msg: types.Message, state: FSMContext):
#     await CreateEvent.title.set()
#     query_params = dict(telegram_id=msg.from_user.id)
#     data = await state.get_data()
#     # pprint(data)
#     response = requests.get(f"http://127.0.0.1:8000/telegram_id/", params=query_params)
#     await state.update_data(id=response.json()[0]['id'])
#     await msg.answer(text='Введите название события',
#                      reply_markup=cancel_button())


# @dp.message_handler(state=CreateEvent.title)
# async def title_state(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['title'] = msg.text
#     await CreateEvent.next()
#     await msg.answer(text='Введите описание события'
#                      )


# @dp.message_handler(state=CreateEvent.description)
# async def desc_state(msg: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['description'] = msg.text
#         await msg.answer('Выберите дату события',
#                          reply_markup=await SimpleCalendar().start_calendar())


# @dp.callback_query_handler(simple_cal_callback.filter(), state=CreateEvent.description)
# async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
#     selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
#     if selected:
#         a = date.strftime('%Y-%m-%d')
#         await state.update_data(chose_date=a)
#         data = await state.get_data()
#         response_data = {'title': data['title'],
#                          'description': data['description'],
#                          'chose_date': data['chose_date'],
#                          'user': data['id']}
#         await state.finish()
#         await callback_query.message.answer(text=f"Событие создано:\n"
#                                                  f"Название: {data['title']}\n"
#                                                  f"Описание: {data['description']}\n"
#                                                  f"Дата: {data['chose_date']}",
#                                             reply_markup=StartKb())
#
#         response = requests.post(f"http://localhost:8000/events/", json=response_data)
#         response.raise_for_status()
#         return response.json()


# @dp.callback_query_handler(Text(contains="get_events", ignore_case=True))
# async def display_events(callback: CallbackQuery):
#     pprint(callback.data)
#     page = int(callback.data.split("_")[-1])
#     response = todo_service.get_events(page)
#
#     rkb = types.InlineKeyboardMarkup(row_width=1)
#
#     for event in response['results']:
#         rkb.add(
#             InlineKeyboardButton(f'{event["title"]}', callback_data=f'display_event:{event["id"]}')
#         )
#
#     pagination_buttons = []
#
#     if response["previous"]:
#         pagination_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"get_events_{page - 1}"))
#     if response["next"]:
#         pagination_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"get_events_{page + 1}"))
#
#     rkb.row(*pagination_buttons).row(types.InlineKeyboardButton("Return", callback_data="return"))
#
#     await callback.message.edit_text("Выберите событие", reply_markup=rkb)


# @dp.callback_query_handler(Text(contains="display_event"))
# async def display_event(callback: types.CallbackQuery, state: FSMContext):
#     event_id = int(callback.data.split(":")[-1])
#     response = todo_service.get_event(event_id)
#     await state.set_state(EventState.event.state)
#     await state.update_data(response, msg_id=callback.message.message_id)
#
#     inline_kb = types.InlineKeyboardMarkup(row_width=1)
#     inline_kb.add(types.InlineKeyboardButton("Изменить ивент", callback_data="change_event"))
#     inline_kb.add(types.InlineKeyboardButton("Вернуться", callback_data="return"))
#
#     await callback.message.edit_text(f'Название: {response["title"]}\n'
#                                      f'Описание: {response["description"]}\n'
#                                      f'Дата события: {response["chose_date"]}',
#                                      reply_markup=inline_kb)
#     await callback.answer("User fetched")
