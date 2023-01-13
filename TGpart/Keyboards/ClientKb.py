from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def StartKb() -> InlineKeyboardButton:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton('Создать событие', callback_data='create_event')
    kb3 = InlineKeyboardButton(text='Показать уже созданные', callback_data='get_events_1')
    kb4 = InlineKeyboardButton('Изменить события', callback_data='vfkwcjbk')
    kb5 = InlineKeyboardButton('Вопросы и пожелания', callback_data='lvjcfblk')
    kb6 = InlineKeyboardButton('Описание', callback_data='ckjwefrbn')
    return kb.add(kb1, kb3, kb6, kb5, kb4)


def cancel_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kb1 = InlineKeyboardButton('Отмена', callback_data='Return')
    return kb.add(kb1)


def show_events() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton(text='Показать', callback_data='get_events_1')
    return kb.add(kb1)
