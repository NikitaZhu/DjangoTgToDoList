from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def start_admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton(text='Посмотреть всех пользователей', callback_data='show_all_admin_users_1')
    kb2 = InlineKeyboardButton(text='Посмотреть все ивенты', callback_data='show_all_admin_events')
    kb3 = InlineKeyboardButton(text='Посмотреть пожелания и вопросы пользователей',  callback_data='show_wishes')
    return kb.add(kb1, kb2, kb3)
