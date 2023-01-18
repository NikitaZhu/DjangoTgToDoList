import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from Keyboards.ClientKb import pop_question
from services.ToDoServices import todo_service


async def pop_a_question(callback: CallbackQuery):
    await callback.message.edit_text('Выберите действие',
                                     reply_markup=pop_question())


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(pop_a_question, Text(equals='pop_a_question'))
