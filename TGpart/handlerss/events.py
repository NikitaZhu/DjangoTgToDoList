import requests
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from Keyboards.ClientKb import cancel_button, StartKb
from services.ToDoServices import todo_service
from states.states import CreateEvent, EventState


async def create_event_cmd(msg: types.Message, state: FSMContext):
    #  Начало стэйта и объявления названия события
    await CreateEvent.title.set()
    query_params = dict(telegram_id=msg.from_user.id)
    data = await state.get_data()
    # pprint(data)
    response = requests.get(f"http://127.0.0.1:8000/telegram_id/", params=query_params)
    await state.update_data(id=response.json()[0]['id'])
    await msg.answer(text='Введите название события',
                     reply_markup=cancel_button())


async def title_state(msg: types.Message, state: FSMContext):
    #  Сохранение названия в дату
    async with state.proxy() as data:
        data['title'] = msg.text
    await CreateEvent.next()
    await msg.answer(text='Введите описание события'
                     )


async def desc_state(msg: types.Message, state: FSMContext):
    #  Объявление описание и сохранение его в дату
    async with state.proxy() as data:
        data['description'] = msg.text
        await msg.answer('Выберите дату события',
                         reply_markup=await SimpleCalendar().start_calendar())


async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    #  Вывод "календаря" с последующим сохранением даты
    if selected:
        a = date.strftime('%Y-%m-%d')
        await state.update_data(chose_date=a)
        data = await state.get_data()
        response_data = {'title': data['title'],
                         'description': data['description'],
                         'chose_date': data['chose_date'],
                         'user': data['id']}
        await state.finish()
        #  Вывод всех данных из даты пользователю
        await callback_query.message.answer(text=f"Событие создано:\n"
                                                 f"Название: {data['title']}\n"
                                                 f"Описание: {data['description']}\n"
                                                 f"Дата: {data['chose_date']}",
                                            reply_markup=StartKb())
        #  Запрос для вывода всех событий пользователю
        response = requests.post(f"http://localhost:8000/events/", json=response_data)
        response.raise_for_status()
        return response.json()


async def display_events(callback: CallbackQuery):
    #  Вывод событий в инлайн кнопках
    page = int(callback.data.split("_")[-1])
    response = todo_service.get_events(page)

    rkb = types.InlineKeyboardMarkup(row_width=1)

    for event in response['results']:
        rkb.add(
            InlineKeyboardButton(f'{event["title"]}', callback_data=f'display_event:{event["id"]}')
        )
    #  Создание кнопок пагинации
    pagination_buttons = []

    if response["previous"]:
        pagination_buttons.append(types.InlineKeyboardButton("⬅️", callback_data=f"get_events_{page - 1}"))
    if response["next"]:
        pagination_buttons.append(types.InlineKeyboardButton("➡️", callback_data=f"get_events_{page + 1}"))

    rkb.row(*pagination_buttons).row(types.InlineKeyboardButton("Return", callback_data="return"))

    await callback.message.edit_text("Выберите событие", reply_markup=rkb)


async def display_event(callback: types.CallbackQuery, state: FSMContext):
    #  Вывод одного ивента при нажатии на кнопку
    event_id = int(callback.data.split(":")[-1])
    response = todo_service.get_event(event_id)
    await state.set_state(EventState.event.state)
    await state.update_data(response, msg_id=callback.message.message_id)

    inline_kb = types.InlineKeyboardMarkup(row_width=1)
    inline_kb.add(types.InlineKeyboardButton("Изменить событие", callback_data="change_event"))
    inline_kb.add(types.InlineKeyboardButton("Вернуться", callback_data="return"))
    #  Отображение всей информации о событии с возможностью изменения его
    await callback.message.edit_text(f'Название: {response["title"]}\n'
                                     f'Описание: {response["description"]}\n'
                                     f'Дата события: {response["chose_date"]}',
                                     reply_markup=inline_kb)
    await callback.answer("User fetched")


# TODO: Сделать обработку кнопок "Изменить событие" и "Вернуться"

def setup(dp: Dispatcher):
    #  Регистрация хэндлеров
    dp.register_message_handler(create_event_cmd, Text(equals='Создать событие'))
    dp.register_message_handler(title_state, state=CreateEvent.title)
    dp.register_message_handler(desc_state, state=CreateEvent.description)
    dp.register_callback_query_handler(process_simple_calendar, simple_cal_callback.filter(),
                                       state=CreateEvent.description)
    dp.register_callback_query_handler(display_events, Text(contains="get_events", ignore_case=True))
    dp.register_callback_query_handler(display_event, Text(contains="display_event"))
