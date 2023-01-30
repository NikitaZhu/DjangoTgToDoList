from pprint import pprint

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Keyboards.Groupskb import groupkb, return_cmd_btn, invite, show_actions

from config import BOT_TOKEN
from services.ToDoServices import todo_service
import requests
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from states.states import Groups

bot = Bot(BOT_TOKEN, parse_mode="HTML")


async def chose_group(callback: CallbackQuery):
    await callback.message.edit_text('Выберите что хотите сделать',
                                     reply_markup=groupkb())


async def cancel_cmd_group(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await callback.bot.send_message(chat_id=callback.message.chat.id,
                                    text='Выбери действие 🎲',
                                    reply_markup=groupkb())
    await callback.message.delete()


async def create_group(callback: CallbackQuery, state: FSMContext):
    await Groups.title.set()
    query_params = dict(telegram_id=callback.from_user.id)
    data = await state.get_data()
    response = requests.get(f"http://127.0.0.1:8000/users/", params=query_params)
    await state.update_data(id=response.json()[0]['id'])

    await callback.message.answer(text='Введите название для группы',
                                  reply_markup=return_cmd_btn())
    await callback.message.delete()


async def group_title(msg: types.Message, state: FSMContext):
    message_id = msg.message_id
    await bot.delete_message(chat_id=msg.chat.id, message_id=message_id - 1)

    async with state.proxy() as data:
        data['title'] = msg.text
    await Groups.next()
    await msg.answer(text='Ведите описание для вашей группы',
                     reply_markup=return_cmd_btn())


async def group_description(msg: types.Message, state: FSMContext):
    message_id = msg.message_id
    await bot.delete_message(chat_id=msg.chat.id, message_id=message_id - 1)

    async with state.proxy() as data:
        data['description'] = msg.text

    data = await state.get_data()
    response_data = {'title': data['title'],
                     'description': data['description'],
                     'user': data['id']}

    await state.finish()
    await msg.answer(text=f'<b>Ваша группа создана:</b>\n'
                          f'\n'
                          f'<b>Название:</b> {data["title"]}\n'
                          f'<b>Описание:</b> {data["description"]}\n'
                          f'\n'
                          f'<b>Что делаем дальше?</b>',
                     reply_markup=invite())

    response = requests.post('http://127.0.0.1:8000/groups/', json=response_data)
    response.raise_for_status()
    return response.json()


async def display_groups(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])
    response = todo_service.get_groups(page)

    ikb = types.InlineKeyboardMarkup(row_width=1)

    for group in response['results']:
        ikb.add(types.InlineKeyboardButton(f'{group["title"]}',
                                           callback_data=f'display_group:{group["id"]}'))
    ikb.add(types.InlineKeyboardButton('Вернуться', callback_data='cancel'))

    await callback.message.edit_text('Выберите группу',
                                     reply_markup=ikb)


async def display_group(callback: CallbackQuery):
    group_id = int(callback.data.split(':')[-1])
    response = todo_service.get_group(group_id)

    await callback.message.edit_text(f'<b>Название: </b>{response["title"]}\n'
                                     f'<b>Описание: </b>{response["description"]}\n'
                                     f'<b>Пользователи: </b>{response["user"]}',
                                     reply_markup=show_actions())


def setup(dp: Dispatcher):
    # dp.register_message_handler(test, Text(equals='test'))
    dp.register_callback_query_handler(chose_group, Text(equals='chose_action_group'))
    dp.register_callback_query_handler(cancel_cmd_group, Text(equals='group_return', ignore_case=True), state='*')
    dp.register_callback_query_handler(create_group, Text(equals='create_group'))
    dp.register_message_handler(group_title, state=Groups.title)
    dp.register_message_handler(group_description, state=Groups.description)
    dp.register_callback_query_handler(display_groups, Text(contains='show_group'))
    dp.register_callback_query_handler(display_group, Text(contains='display_group'))
