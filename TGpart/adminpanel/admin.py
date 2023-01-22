import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Keyboards.adminkb import start_admin_kb, cancel_admin
from config import admin_id
from services.ToDoServices import todo_service


async def admin_cmd(msg: types.Message):
    if msg.from_user.id == admin_id:
        await msg.answer(text='Вы зашли в админку',
                         reply_markup=start_admin_kb())
        await msg.delete()
    else:
        await msg.delete()
        await msg.answer(text='Вы не являетесь администратором.')


async def display_users(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])
    response = todo_service.get_users(page)

    rkb = InlineKeyboardMarkup(row_width=1)

    for users in response['results']:
        rkb.add(
            InlineKeyboardButton(f'{users["id"]}. {users["full_name"]}', callback_data=f'display_user:{users["id"]}')
        )

    pagination_buttons = []

    if response["previous"]:
        pagination_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"show_all_admin_users_{page - 1}"))
    if response["next"]:
        pagination_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"show_all_admin_users_{page + 1}"))

    rkb.row(*pagination_buttons).row(
        types.InlineKeyboardButton("Вернуться", callback_data='exit', ignore_case=True))

    await callback.message.edit_text(text='Все пожелания и вопросы пользователей',
                                     reply_markup=rkb)


async def show_wishes(callback: CallbackQuery):
    page = int(callback.data.split("_")[-1])
    response = todo_service.get_questions(page)

    rkb = InlineKeyboardMarkup(row_width=1)

    for ques in response['results']:
        rkb.add(
            InlineKeyboardButton(f'{ques["id"]}. {ques["description"]}', callback_data=f'display_wish:{ques["id"]}')
        )

    pagination_buttons = []

    if response["previous"]:
        pagination_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"show_wishes_{page - 1}"))
    if response["next"]:
        pagination_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"show_wishes_{page + 1}"))

    rkb.row(*pagination_buttons).row(
        types.InlineKeyboardButton("Вернуться", callback_data='exit', ignore_case=True))

    await callback.message.edit_text(text='Все пожелания и вопросы пользователей',
                                     reply_markup=rkb)


async def display_wish(callback: CallbackQuery):
    wish_id = int(callback.data.split(':')[-1])
    response = todo_service.get_wish(wish_id)

    s = str(f'Полная информация:\n'
            f'Вопрос пользователя: {response["description"]}\n'
            )

    if int(callback.from_user.id) == 469426848:
        response_user = requests.get(f'http://127.0.0.1:8000/users/{response["user"]}/')
        s += f'Никнэйм: @{response_user.json()["username"]}'

    await callback.message.edit_text(s, reply_markup=start_admin_kb())


async def show_user(callback: CallbackQuery):
    users_id = int(callback.data.split(':')[-1])

    response = todo_service.get_user(users_id)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Вернуться", callback_data="exit"))
    #  Отображение всей информации о событии с возможностью изменения его
    await callback.message.edit_text(f'Полное имя: {response["full_name"]}\n'
                                     f'телеграм_id: {response["telegram_id"]}\n'
                                     f'Ник: @{response["username"]}',
                                     reply_markup=inline_kb)
    await callback.answer("User fetched")


async def display_events_admin(callback: CallbackQuery):
    #  Вывод событий в инлайн кнопках
    page = int(callback.data.split("_")[-1])
    response = todo_service.get_events(page)

    rkb = types.InlineKeyboardMarkup(row_width=1)

    for event in response['results']:
        rkb.add(
            InlineKeyboardButton(f'{event["title"]}', callback_data=f'display_event_admin:{event["id"]}')
        )
        #  Создание кнопок пагинации
    pagination_buttons = []

    if response["previous"]:
        pagination_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"show_all_admin_events_{page - 1}"))
    if response["next"]:
        pagination_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"show_all_admin_events_{page + 1}"))

    rkb.row(*pagination_buttons).row(
        types.InlineKeyboardButton("Вернуться", callback_data='Cancel', ignore_case=True))

    await callback.message.edit_text("Выберите событие", reply_markup=rkb)


async def display_event_admin(callback: types.CallbackQuery, state: FSMContext):
    query_params = dict(telegram_id=callback.from_user.id)
    response = requests.get(f"http://127.0.0.1:8000/users/", params=query_params)

    user_id = response.json()[0]['id']
    event_id = int(callback.data.split(":")[-1])
    response = requests.get(f"http://127.0.0.1:8000/events/{event_id}")
    response = todo_service.get_event(event_id)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Удалить событие", callback_data=f"delete_event_{event_id}"))
    inline_kb.add(types.InlineKeyboardButton("Вернуться", callback_data="Cancel"))
    #  Отображение всей информации о событии с возможностью изменения его
    await callback.message.edit_text(f'Название: {response["title"]}\n'
                                     f'Описание: {response["description"]}\n'
                                     f'Дата события: {response["chose_date"]}',
                                     reply_markup=inline_kb)
    await callback.answer("User fetched")


def setup(dp: Dispatcher):
    dp.register_message_handler(admin_cmd, commands=['admin'])
    dp.register_callback_query_handler(display_users, Text(contains='show_all_admin_users'))
    dp.register_callback_query_handler(show_wishes, Text(contains='show_wishes'))
    dp.register_callback_query_handler(show_user, Text(contains='display_user'))
    dp.register_callback_query_handler(display_wish, Text(contains='display_wish'))
    dp.register_callback_query_handler(display_events_admin, Text(contains="show_all_admin_events", ignore_case=True))
    dp.register_callback_query_handler(display_event_admin, Text(contains="display_event_admin"))
