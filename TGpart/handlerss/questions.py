import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from Keyboards.ClientKb import pop_question, StartKb
from services.ToDoServices import todo_service
from states.states import CreateWish


async def pop_a_question(callback: CallbackQuery):
    await callback.message.edit_text('Выберите действие',
                                     reply_markup=pop_question())


async def client_wish(callback: CallbackQuery, state: FSMContext):
    await CreateWish.desc.set()

    query_params = dict(telegram_id=callback.from_user.id)
    data = await state.get_data()
    response = requests.get(f"http://127.0.0.1:8000/users/", params=query_params)
    await state.update_data(id=response.json()[0]['id'])

    await callback.message.edit_text('Задайте ваш вопрос',
                                     )
    async with state.proxy() as data:
        data['description'] = callback.message.text


async def client_question(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = msg.text
    data = await state.get_data()
    response_data = {'description': data['description'],
                     'user': data['id']}
    await state.finish()
    await msg.answer('Ваш вопрос отправлен администратору.\n'
                     'Ответ придёт в течении суток',
                     reply_markup=StartKb())

    response = requests.post('http://localhost:8000/questions/', json=response_data)
    response.raise_for_status()
    return response.json()


async def client_wishes(callback: CallbackQuery, state: FSMContext):
    await CreateWish.wish.set()
    query_params = dict(telegram_id=callback.from_user.id)
    data = await state.get_data()
    response = requests.get(f"http://127.0.0.1:8000/users/", params=query_params)
    await state.update_data(id=response.json()[0]['id'])

    await callback.message.edit_text('Оставьте свой совет здесь',)
    async with state.proxy() as data:
        data['description'] = callback.message.text


async def client_questions(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = msg.text
    data = await state.get_data()
    response_data = {'description': data['description'],
                     'user': data['id']}
    await state.finish()
    await msg.answer('Ваш совет отправлен администратору\n'
                     'Спасибо за поддержку ❤️',
                     reply_markup=StartKb())

    response = requests.post('http://localhost:8000/questions/', json=response_data)
    response.raise_for_status()
    return response.json()


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(pop_a_question, Text(equals='pop_a_question'))
    dp.register_callback_query_handler(client_wish, Text(equals='question'))
    dp.register_message_handler(client_question, state=CreateWish.desc)
    dp.register_callback_query_handler(client_wishes, Text(equals='tip'))
    dp.register_message_handler(client_questions, state=CreateWish.wish)
