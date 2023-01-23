from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def groupkb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton(text='Создать группу', callback_data='create_group')
    kb2 = InlineKeyboardButton(text='Посмотреть группы', callback_data='show_group_1')
    kb3 = InlineKeyboardButton(text='Вернуться', callback_data='cancel')
    return kb.add(kb1, kb2, kb3)


def return_cmd_btn() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton('Отмена', callback_data='group_return')
    return kb.add(kb1)


def invite() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton('Создать групповое событие', callback_data='create_group_event')
    kb2 = InlineKeyboardButton('Пригласить человека в группу', callback_data='invite_people')
    kb3 = InlineKeyboardButton('Посмотреть всех участников', callback_data='show_all_members')
    kb4 = InlineKeyboardButton('Вернуться в главное меню', callback_data='cancel')
    return kb.add(kb1, kb2, kb3, kb4)


def show_actions() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb5 = InlineKeyboardButton('Создать событие группы', callback_data='create_group_event')
    kb1 = InlineKeyboardButton('Изменить название', callback_data='change_title_group')
    kb2 = InlineKeyboardButton('Изменить описание', callback_data='change_desc_group')
    kb3 = InlineKeyboardButton('Пригласить человека', callback_data='invite_person_group')
    kb4 = InlineKeyboardButton('В главное меню', callback_data='cancel')
    return kb.add(kb1, kb2, kb3, kb4)
