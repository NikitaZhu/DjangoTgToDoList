from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Keyboards.adminkb import start_admin_kb
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
            InlineKeyboardButton(f'{ques["id"]}. {ques["description"]}', callback_data=f'show_quiz:{ques["id"]}')
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


def setup(dp: Dispatcher):
    dp.register_message_handler(admin_cmd, commands=['admin'])
    dp.register_callback_query_handler(display_users, Text(contains='show_all_admin_users'))
    dp.register_callback_query_handler(show_wishes, Text(contains='show_wishes'))
