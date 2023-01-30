from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateEvent(StatesGroup):
    title = State()
    description = State()
    date = State()


class ChangeEvent(StatesGroup):
    event = State()
    title = State()
    description = State()
    date = State()


class CreateWish(StatesGroup):
    desc = State()
    wish = State()


class Groups(StatesGroup):
    title = State()
    description = State()


class Notifications(StatesGroup):
    description = State()
