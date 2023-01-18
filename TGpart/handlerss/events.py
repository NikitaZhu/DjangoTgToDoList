from pprint import pprint

import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from Keyboards.ClientKb import cancel_button, StartKb, change_kb
from config import admin_id
from services.ToDoServices import todo_service
from states.states import CreateEvent, ChangeEvent


async def create_event_cmd(callback: CallbackQuery, state: FSMContext):
    #  Начало стэйта и объявления названия события
    await CreateEvent.title.set()
    query_params = dict(telegram_id=callback.from_user.id)
    data = await state.get_data()
    # pprint(data)
    response = requests.get(f"http://127.0.0.1:8000/users/", params=query_params)
    await state.update_data(id=response.json()[0]['id'])
    await callback.message.answer(text='Введите название события',
                                  reply_markup=cancel_button())
    await callback.message.delete()


async def title_state(msg: types.Message, state: FSMContext):
    #  Сохранение названия в дату
    async with state.proxy() as data:
        data['title'] = msg.text
    await CreateEvent.next()
    await msg.answer(text='Введите описание события',
                     reply_markup=cancel_button()
                     )


async def desc_state(msg: types.Message, state: FSMContext):
    #  Объявление описание и сохранение его в дату
    async with state.proxy() as data:
        data['description'] = msg.text
        await msg.answer('Выберите дату события',
                         reply_markup=await SimpleCalendar().start_calendar())


async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    #  Вывод "календаря" с последующим сохранением даты
    if selected:
        a = date.strftime('%Y-%m-%d')
        await state.update_data(chose_date=a)
        data = await state.get_data()
        response_data = {'title': data['title'],
                         'description': data['description'],
                         'chose_date': data['chose_date'],
                         'user': data['id']}
        await state.finish()
        #  Вывод всех данных из даты пользователю
        await callback_query.message.answer(text=f"Событие создано:\n"
                                                 f"Название: {data['title']}\n"
                                                 f"Описание: {data['description']}\n"
                                                 f"Дата: {data['chose_date']}",
                                            reply_markup=StartKb())
        #  Запрос для вывода всех событий пользователю
        response = requests.post(f"http://localhost:8000/events/", json=response_data)
        response.raise_for_status()
        return response.json()


async def display_events(callback: CallbackQuery):
    #  Вывод событий в инлайн кнопках
    if callback.from_user.id == admin_id:
        page = int(callback.data.split("_")[-1])
        response = todo_service.get_events(page)

        rkb = types.InlineKeyboardMarkup(row_width=1)

        for event in response['results']:
            rkb.add(
                InlineKeyboardButton(f'{event["title"]}', callback_data=f'display_event:{event["id"]}')
            )

        #  Создание кнопок пагинации
        pagination_buttons = []

        if response["previous"]:
            pagination_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"get_events_{page - 1}"))
        if response["next"]:
            pagination_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"get_events_{page + 1}"))

        rkb.add(InlineKeyboardButton('Показать мои события', callback_data='show_my_events_1'))

        rkb.row(*pagination_buttons).row(
            types.InlineKeyboardButton("Вернуться", callback_data='Cancel', ignore_case=True))

        await callback.message.edit_text("Выберите событие", reply_markup=rkb)
    else:
        query_params = dict(telegram_id=callback.from_user.id)
        response = requests.get(f"http://127.0.0.1:8000/users/", params=query_params)
        page = int(callback.data.split("_")[-1])
        event_data = {'page': page, 'user': response.json()[0]['id']}
        response = todo_service.get_my_events(event_data)

        rkb = types.InlineKeyboardMarkup(row_width=1)

        for event in response['results']:
            rkb.add(
                InlineKeyboardButton(f'{event["title"]}', callback_data=f'display_event:{event["id"]}')
            )
        #  Создание кнопок пагинации
        pagination_buttons = []

        if response["previous"]:
            pagination_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"show_my_events_{page - 1}"))
        if response["next"]:
            pagination_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"show_my_events_{page + 1}"))

        rkb.row(*pagination_buttons).row(
            types.InlineKeyboardButton("Вернуться", callback_data='Cancel', ignore_case=True))

        await callback.message.edit_text("Выберите событие", reply_markup=rkb)


# async def display_my_events(callback: CallbackQuery):
#     #  Вывод событий в инлайн кнопках
#     query_params = dict(telegram_id=callback.from_user.id)
#     response = requests.get(f"http://127.0.0.1:8000/users/", params=query_params)
#     page = int(callback.data.split("_")[-1])
#     event_data = {'page': page, 'user': response.json()[0]['id']}
#     response = todo_service.get_my_events(event_data)
#
#     rkb = types.InlineKeyboardMarkup(row_width=1)
#
#     for event in response['results']:
#         rkb.add(
#             InlineKeyboardButton(f'{event["title"]}', callback_data=f'display_event:{event["id"]}')
#         )
#     #  Создание кнопок пагинации
#     pagination_buttons = []
#
#     if response["previous"]:
#         pagination_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"show_my_events_{page - 1}"))
#     if response["next"]:
#         pagination_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"show_my_events_{page + 1}"))
#
#     rkb.row(*pagination_buttons).row(types.InlineKeyboardButton("Вернуться", callback_data='Cancel', ignore_case=True))
#
#     await callback.message.edit_text("Выберите событие", reply_markup=rkb)
#

async def display_event(callback: types.CallbackQuery, state: FSMContext):
    #  Вывод одного ивента при нажатии на кнопку
    query_params = dict(telegram_id=callback.from_user.id)
    response = requests.get(f"http://127.0.0.1:8000/users/", params=query_params)

    user_id = response.json()[0]['id']
    event_id = int(callback.data.split(":")[-1])
    response = requests.get(f"http://127.0.0.1:8000/events/{event_id}")
    if user_id == response.json()['user']:
        response = todo_service.get_event(event_id)
        await state.set_state(ChangeEvent.event.state)

        inline_kb = types.InlineKeyboardMarkup(row_width=1)
        inline_kb.add(types.InlineKeyboardButton("Изменить событие", callback_data=f"change_event_{event_id}"))
        inline_kb.add(types.InlineKeyboardButton("Вернуться", callback_data="Cancel"))
        await state.finish()
        #  Отображение всей информации о событии с возможностью изменения его
        await callback.message.edit_text(f'Название: {response["title"]}\n'
                                         f'Описание: {response["description"]}\n'
                                         f'Дата события: {response["chose_date"]}',
                                         reply_markup=inline_kb)
        await callback.answer("User fetched")
    else:
        response = todo_service.get_event(event_id)
        await state.set_state(ChangeEvent.event.state)

        inline_kb = types.InlineKeyboardMarkup(row_width=1)
        inline_kb.add(types.InlineKeyboardButton("Вернуться", callback_data="Return"))
        await state.finish()
        #  Отображение всей информации о событии с возможностью изменения его
        await callback.message.edit_text(f'Название: {response["title"]}\n'
                                         f'Описание: {response["description"]}\n'
                                         f'Дата события: {response["chose_date"]}',
                                         reply_markup=inline_kb)
        await callback.answer("User fetched")


async def change_event(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(event_id=callback.data.split('_')[-1])
    await callback.message.answer(text='Что изменить?',
                                  reply_markup=change_kb())


async def change_title(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Введите новое название',
                                  reply_markup=cancel_button())
    await ChangeEvent.title.set()
    await state.update_data(field='title')
    await state.finish()


async def change_description(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Введите новое описание',
                                  reply_markup=cancel_button())
    await ChangeEvent.description.set()
    await state.update_data(field='description')


async def change_date(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(text='Введите новую дату',
                                  reply_markup=cancel_button())
    await ChangeEvent.date.set()
    await state.update_data(field='date')


async def patch_event(msg: types.Message, state: FSMContext):
    get_data = await state.get_data()
    if get_data['field'] == 'title':
        title = msg.text
        event_data = {'id': get_data['event_id'], 'title': title}
        response = todo_service.patch_event(event_data)
        await state.finish()
        await msg.answer(text='Название изменено. Что делаем дальше?',
                         reply_markup=change_kb())

    elif get_data['field'] == 'description':
        description = msg.text
        event_data = {'id': get_data['event_id'], 'description': description}
        response = todo_service.patch_event(event_data)
        await state.finish()
        await msg.answer(text='Описание изменено. Что делаем дальше?',
                         reply_markup=change_kb())

    elif get_data['field'] == 'date':
        date = msg.text
        event_data = {'id': get_data['event_id'], 'chose_date': date}
        response = todo_service.patch_event(event_data)
        await state.finish()
        await msg.answer(text='Дата изменена. Что делаем дальше?',
                         reply_markup=change_kb())


def setup(dp: Dispatcher):
    #  Регистрация хэндлеров
    dp.register_callback_query_handler(create_event_cmd, Text(equals='create_event'))
    dp.register_message_handler(title_state, state=CreateEvent.title)
    dp.register_message_handler(desc_state, state=CreateEvent.description)
    dp.register_callback_query_handler(process_simple_calendar, simple_cal_callback.filter(),
                                       state=CreateEvent.description)
    dp.register_callback_query_handler(display_events, Text(contains="get_events", ignore_case=True))
    # dp.register_callback_query_handler(display_my_events, Text(contains='show_my_events', ignore_case=True))
    dp.register_callback_query_handler(display_event, Text(contains="display_event"))
    dp.register_callback_query_handler(change_event, Text(contains='change_event'))
    dp.register_callback_query_handler(change_title, Text(equals='change_title'))
    dp.register_callback_query_handler(change_description, Text(equals='change_desc'))
    dp.register_callback_query_handler(change_date, Text(equals='change_date'))
    dp.register_message_handler(patch_event, state=ChangeEvent.title)
    dp.register_message_handler(patch_event, state=ChangeEvent.description)
    dp.register_message_handler(patch_event, state=ChangeEvent.date)
