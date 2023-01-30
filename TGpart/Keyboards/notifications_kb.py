from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def set_notice() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton('Проверить уведомления', callback_data='show_notifications_1')
    kb2 = InlineKeyboardButton('Создать уведомление', callback_data='create_notification')
    kb3 = InlineKeyboardButton('Вернуться', callback_data='cancel')
    return kb.add(kb1, kb2, kb3)


def settings_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton('Каждый день', callback_data='every_day')
    kb2 = InlineKeyboardButton('В определённый день каждую неделю', callback_data='every_week')
    kb3 = InlineKeyboardButton('С интервалом времени', callback_data='interval_time')
    kb4 = InlineKeyboardButton('Вернуться', callback_data='cancel')
    return kb.add(kb1, kb2, kb3, kb4)


def cancel_notice() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton('Отмена', callback_data='return')
    return kb.add(kb1)


def every_week_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=1)
    kb1 = InlineKeyboardButton('Понедельник', callback_data='monday')
    kb2 = InlineKeyboardButton('Вторник', callback_data='tuersday')
    kb3 = InlineKeyboardButton('Среда', callback_data='wednesday')
    kb4 = InlineKeyboardButton('Четверг', callback_data='thusday')
    kb5 = InlineKeyboardButton('Пятница', callback_data='friday')
    kb6 = InlineKeyboardButton('Суббота', callback_data='saturday')
    kb7 = InlineKeyboardButton('Воскресенье', callback_data='sunday')
    kb8 = InlineKeyboardButton('Отмена', callback_data='cancel')
    return kb.add(kb1, kb2, kb3, kb4, kb5, kb6, kb7, kb8)
