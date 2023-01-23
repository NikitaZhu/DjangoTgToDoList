from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def StartKb() -> InlineKeyboardButton:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton('🎆  Создать событие', callback_data='create_event')
    kb3 = InlineKeyboardButton(text='✨  Показать уже созданные', callback_data='show_my_events_1')
    kb5 = InlineKeyboardButton('❔  Вопросы и пожелания', callback_data='pop_a_question')
    kb6 = InlineKeyboardButton('🤖  Описание', callback_data='descc')
    kb7 = InlineKeyboardButton('🥳  Группы(в разработке)', callback_data='chose_action_group')
    return kb.add(kb1, kb3, kb6, kb5, kb7)


def cancel_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    kb1 = InlineKeyboardButton('Отмена', callback_data='Return')
    return kb.add(kb1)


def show_events() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton(text='Показать', callback_data='t_vents_1')
    return kb.add(kb1)


def change_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton('Изменить название', callback_data='change_title')
    kb2 = InlineKeyboardButton('Изменить описание', callback_data='change_desc')
    kb3 = InlineKeyboardButton('Изменить дату', callback_data='change_date')
    kb4 = InlineKeyboardButton('Отмена', callback_data='Cancel')
    return kb.add(kb1, kb2, kb3, kb4)


def pop_question() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton('Задать вопрос', callback_data='question')
    kb2 = InlineKeyboardButton('Совет по улучшению Бота', callback_data='tip')
    kb3 = InlineKeyboardButton('Вернуться', callback_data='cancel')
    return kb.add(kb1, kb2, kb3)
