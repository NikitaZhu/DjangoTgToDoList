from pprint import pprint

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Keyboards.notifications_kb import set_notice, settings_kb, cancel_notice, every_week_kb
from config import BOT_TOKEN
from services.ToDoServices import todo_service
import requests
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from states.states import Notifications

empty = []


async def set_notifications(callback: CallbackQuery):
    """Просмотр и настройка уведомлений"""

    await callback.message.edit_text(text='<b>💌  Настройки уведомлений</b>',
                                     reply_markup=set_notice())


async def show_my_notifications(callback: CallbackQuery):
    """Запрос на отображение созданных уведомлений"""
    response = requests.get(url='http://127.0.0.1:8000/notifications/')
    if response.json() == empty:
        await callback.message.answer(text='<b>У вас пока что нет активных уведомлений</b> ☹️')
    else:
        page = int(callback.data.split('_')[-1])
        response_id = todo_service.get_notifications(page)

        ikb = types.InlineKeyboardMarkup(row_width=1)

        for notice in response_id['results']:
            ikb.add(types.InlineKeyboardButton(f'{notice["description"]}',
                                               callback_data=f'notice_id:{notice["id"]}'))
        ikb.add(types.InlineKeyboardButton('Вернуться в главное меню', callback_data='Cancel'))

        await callback.message.edit_text('<b>Что выбираете ❓</b>',
                                         reply_markup=ikb)


async def create_notifications(callback: CallbackQuery, state: FSMContext):
    """Создание уведомлений"""
    await Notifications.description.set()
    query_params = dict(telegram_id=callback.from_user.id)
    data = await state.get_data()
    response = requests.get(url='http://127.0.0.1:8000/users/', params=query_params)
    await state.update_data(id=response.json()[0]['id'])

    await callback.message.edit_text('<b>Тут напишите о чём вам напомнить</b>',
                                     reply_markup=cancel_notice())


async def notification_desc(msg: types.Message, state: FSMContext):
    """Сохранение введённых пользователем данных"""
    async with state.proxy() as data:
        data['description'] = msg.text

    await state.get_data()
    response_json = {'description': data['description'],
                     'user': data['id']}
    await state.finish()
    await msg.answer(f'<b>Теперь давайте настроим когда вам об этом напоминать</b>\n'
                     f'{data["description"]}',
                     reply_markup=settings_kb())

    response = requests.post('http://127.0.0.1:8000/notifications/', json=response_json)
    response.raise_for_status()
    return response.json()


async def show_notification(callback: CallbackQuery):
    notice_id = int(callback.data.split(':')[-1])
    response = todo_service.get_notification(notice_id)

    await callback.message.answer(f'<b>Давайте настроим когда вам напоминать об этом:</b>\n'
                                  f'<em>{response["description"]}</em>',
                                  reply_markup=settings_kb())


async def every_week(callback: CallbackQuery):
    await callback.message.edit_text('<b>В какой день вам напоминать об этом?</b>',
                                     reply_markup=every_week_kb())


def setup(dp: Dispatcher):
    """Регистрация хэндлеров"""
    dp.register_callback_query_handler(set_notifications, Text(equals='set_notifications'))
    dp.register_callback_query_handler(show_my_notifications, Text(contains='show_notifications'))
    dp.register_callback_query_handler(create_notifications, Text(equals='create_notification'))
    dp.register_message_handler(notification_desc, state=Notifications.description)
    dp.register_callback_query_handler(show_notification, Text(contains='notice_id'))
    dp.register_callback_query_handler(every_week, Text(equals='every_week'))
