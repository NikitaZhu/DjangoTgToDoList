from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateEvent(StatesGroup):
    title = State()
    description = State()
    date = State()


class EventState(StatesGroup):
    event = State()
    title = State()
