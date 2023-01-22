from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def start_admin_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton(text='Посмотреть всех пользователей', callback_data='show_all_admin_users_1')
    kb2 = InlineKeyboardButton(text='Посмотреть все ивенты', callback_data='show_all_admin_events_1')
    kb3 = InlineKeyboardButton(text='Посмотреть пожелания и вопросы пользователей', callback_data='show_wishes_1')
    return kb.add(kb1, kb2, kb3)


def are_u_sure_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton('Да', callback_data=f'delete_event')
    kb2 = InlineKeyboardButton('Нет', callback_data='no')
    return kb.add(kb1, kb2)


def cancel_admin() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb2 = InlineKeyboardButton('Вернуться', callback_data='exit')
    return kb.add(kb2)
