from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def StartKb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb1 = KeyboardButton('Создать событие')
    kb3 = KeyboardButton('Показать уже созданные события')
    kb4 = KeyboardButton('Изменить события')
    kb5 = KeyboardButton('Вопросы и пожелания')
    kb6 = KeyboardButton('Описание')
    return kb.row(kb1).row(kb3).row(kb4).row(kb5, kb6)


def CalendarKB() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb1 = InlineKeyboardButton('Открыть календарь', callback_data='open_calendar')
    return kb.add(kb1)


def cancel_button() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb1 = KeyboardButton('Вернуться в главное меню')
    return kb.add(kb1)
