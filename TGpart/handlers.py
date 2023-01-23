import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from Keyboards.adminkb import start_admin_kb
from Keyboards.ClientKb import StartKb
from app import bot, dp, types


@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message):
    user = msg.from_user
    data = dict(username=user.username, telegram_id=user.id, full_name=user.full_name)
    res = requests.post("http://127.0.0.1:8000/users/", data=data)
    user = res.json()

    await bot.send_sticker(sticker='CAACAgIAAxkBAAEG9kFjpYem9AABYNWO9Ts1qFDXvqhTpRsAAkIQAAIzxSlJkA7UEacqSoIsBA',
                           chat_id=msg.chat.id)
    await bot.send_message(chat_id=msg.chat.id,
                           text='<b>Выбери действие</b> 🎲',
                           reply_markup=StartKb())
    await msg.delete()


@dp.callback_query_handler(Text(equals='Return', ignore_case=True), state='*')
async def cancel_cmd(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await callback.bot.send_message(chat_id=callback.message.chat.id,
                                    text='<b>Выбери действие</b> 🎲',
                                    reply_markup=StartKb())
    await callback.message.delete()


@dp.callback_query_handler(Text(equals='cancel', ignore_case=True))
async def return_cmd(callback: CallbackQuery):
    await callback.message.edit_text(text='<b>Выбери действие</b> 🎲',
                                     reply_markup=StartKb())


@dp.callback_query_handler(Text(equals='exit', ignore_case=True))
async def admin_cancel(callback: CallbackQuery):
    await callback.message.edit_text(text='Вы зашли в админку',
                                     reply_markup=start_admin_kb())


@dp.callback_query_handler(Text(equals='descc', ignore_case=True))
async def desc_cmd(callback: CallbackQuery):
    await callback.message.answer('Этот бот умеет создавать и хранить ваши запланированные события.')
