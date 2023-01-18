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
            InlineKeyboardButton(f'{users["id"]}. {users["full_name"]}', callback_data=f'display_users_{users["id"]}')
        )

    await callback.message.answer(text='Все пользователи', reply_markup=rkb)


def setup(dp: Dispatcher):
    dp.register_message_handler(admin_cmd, commands=['admin'])
    dp.register_callback_query_handler(display_users, Text(contains='show_all_admin_users'))
