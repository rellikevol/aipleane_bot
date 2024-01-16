from aiogram import types, Dispatcher
from telegram_bot.utils import menu
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from telegram_bot.globals import db_name, global_check_date_year, count_of_description
from telegram_bot.keyboards import cancel_menu
from telegram_bot.utils import cancel, count_symbols
from telegram_bot.utils import find_town, change_town
from telegram_bot.create_bot import storage, bot
from telegram_bot.database import date_to_digts, insert_carry, find_send_while_create
from telegram_bot.messages import print_suitable_carry_request, carry_request_are_registered
from datetime import datetime as dt
from datetime import date
from telegram_bot.calendar_test import calendar_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class States_for_courier(StatesGroup):
    point_search = State()
    point_pos = State()
    point_len = State()
    point_message_id = State()
    point_from = State()
    point_to = State()
    description = State()
    date = State()
    price = State()


async def carry(callback: types.CallbackQuery):
    await States_for_courier.point_search.set()
    await callback.message.answer(f'Укажите город, из которого вы отправляетесь:', reply_markup=cancel_menu)


async def carry_set_from_search(message: types.Message, state: FSMContext):
    if await find_town(message, state):
        res = await storage.get_data(user=message.from_user.id)
        if 'point_from' in res:
            await States_for_courier.point_to.set()
        else:
            await States_for_courier.point_from.set()


# --------------- point from ----------------------

async def town_from_check_carry(callback: types.CallbackQuery, state: FSMContext):
    await change_town(callback, state)


async def town_from_set_carry(callback: types.CallbackQuery, state: FSMContext):
    res = await storage.get_data(user=callback.from_user.id)
    await state.update_data(point_from=res['point_search'][res['point_pos']])
    await callback.message.answer(f'Укажите город, в который вы отправляетесь:', reply_markup=cancel_menu)
    await States_for_courier.point_search.set()


# ----------------------------- point to --------------------

async def town_to_check_carry(callback: types.CallbackQuery, state: FSMContext):
    await change_town(callback, state)


async def town_to_set_carry(callback: types.CallbackQuery, state: FSMContext):
    res = await storage.get_data(user=callback.from_user.id)
    await state.update_data(point_to=res['point_search'][res['point_pos']])
    await callback.message.answer(f'Опишите, что вы готовы доставить? '
                                  f'<i>(не более {count_of_description} символов)</i>', reply_markup=cancel_menu,
                                  parse_mode=types.ParseMode.HTML)
    await States_for_courier.description.set()


async def carry_set_description(message: types.Message, state: FSMContext):
    if count_symbols(message.text):
        await state.update_data(description=message.text)
        await States_for_courier.date.set()
        date_message_id = await bot.send_message(
            message.chat.id,
            f'Выберите дату вашей поездки:',
            reply_markup=calendar_keyboard(year=dt.today().year.real, month=dt.today().month.real),
            parse_mode=types.ParseMode.HTML
        )
        await state.update_data(date=dt.today())
    else:
        await message.answer(
            f'Это описание слишком длинное, попробуйте описать короче... '
            f'<i>(не более {count_of_description} символов)</i>',
            reply_markup=cancel_menu,
            parse_mode=types.ParseMode.HTML
        )


async def carry_set_date(callback: types.CallbackQuery, state: FSMContext):
    res = await storage.get_data(user=callback.from_user.id)
    year = res['date'].year.real
    month = res['date'].month.real

    if callback.data == 'without_date':
        await state.update_data(date=False)
        await callback.message.answer(f'Укажите валюту оплаты и цену за ваши услуги:', reply_markup=cancel_menu)
        await States_for_courier.price.set()

    if callback.data == 'calendar_previous_month':
        if month == 1:
            year = year - 1
            month = 12
        else:
            month = month - 1

        await bot.edit_message_reply_markup(
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=calendar_keyboard(year, month)
        )
        await state.update_data(date=date(year, month, 1))

    if callback.data == 'calendar_next_month':
        if month == 12:
            year = year + 1
            month = 1
        else:
            month = month + 1

        await bot.edit_message_reply_markup(
            callback.message.chat.id,
            callback.message.message_id,
            reply_markup=calendar_keyboard(year, month)
        )
        await state.update_data(date=date(year, month, 1))

    if callback.data[0] == 'D':
        date_one = date_to_digts(callback.data[2:])
        date_two = date(date_one[2], date_one[1], date_one[0])
        date_max_period = date(date.today().year + global_check_date_year, date.today().month, date.today().day)

        if date.today() > date_two:
            await callback.message.answer(
                f'Этот день уже прошел. Попробуйте ещё раз...',
                parse_mode=types.ParseMode.HTML
            )
        else:
            if date_two > date_max_period:
                await callback.message.answer(
                    f'Это слишком далёкая дата. Пожалуйста, выберите дату не позднее:\n\n '
                    f'<b>{date_max_period.strftime("%d.%m.%Y")}</b>.',
                    parse_mode=types.ParseMode.HTML
                )
            else:
                await state.update_data(date=date_one)
                await callback.message.answer(
                    f'Укажите валюту оплаты и цену за ваши услуги:',
                    reply_markup=cancel_menu
                )
                await States_for_courier.price.set()


async def carry_set_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    res = await storage.get_data(user=message.from_user.id)

    # ------------------- запись в базу ---------------------
    if res['date']:
        insert_carry(db_name, message.from_user.id, message.from_user.username, message.chat.id, "carry",
                     res['point_from']['town'], res['point_from']['state'], res['point_from']['country'],
                     res['point_to']['town'], res['point_to']['state'], res['point_to']['country'],
                     res['description'], 'created', res['price'], dt.now().year, dt.now().month, dt.now().day,
                     res['date'][2], res['date'][1], res['date'][0])
    else:
        insert_carry(db_name, message.from_user.id, message.from_user.username, message.chat.id, "carry",
                     res['point_from']['town'], res['point_from']['state'], res['point_from']['country'],
                     res['point_to']['town'], res['point_to']['state'], res['point_to']['country'],
                     res['description'], 'created', res['price'], dt.now().year, dt.now().month, dt.now().day,
                     None, None, None)

    send_one = find_send_while_create(db_name,
                                      res['point_from']['town'], res['point_from']['state'],
                                      res['point_from']['country'],
                                      res['point_to']['town'], res['point_to']['state'], res['point_to']['country'])
    if len(send_one) != 0:
        for i in send_one:
            if i != message.from_user.id:

                answer_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
                button_two = InlineKeyboardButton("Написать пользователю", url=f'tg://user?id={message.from_user.id}')
                answer_keyboard.add(button_two)

                await bot.send_message(i, print_suitable_carry_request(
                    res['point_from']['town'], res['point_from']['state'], res['point_from']['country'],
                    res['point_to']['town'], res['point_to']['state'], res['point_to']['country'],
                    message.from_user.username, res['description'], res['price'], res['date']
                ), parse_mode=types.ParseMode.HTML, reply_markup=answer_keyboard)

    await message.answer(carry_request_are_registered(), parse_mode=types.ParseMode.HTML)
    await state.finish()
    await menu(message)


async def carry_cancel(callback: types.CallbackQuery, state: FSMContext):
    await cancel(callback, state)


# -------------------------------------

def register_create_carry_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(carry, text=['create_carry'])
    dp.register_message_handler(carry_set_from_search, state=States_for_courier.point_search)
    dp.register_callback_query_handler(town_from_check_carry, text=['town_no'], state=States_for_courier.point_from)
    dp.register_callback_query_handler(town_from_set_carry, text=['town_yes'], state=States_for_courier.point_from)
    dp.register_callback_query_handler(town_to_check_carry, text=['town_no'], state=States_for_courier.point_to)
    dp.register_callback_query_handler(town_to_set_carry, text=['town_yes'], state=States_for_courier.point_to)
    dp.register_message_handler(carry_set_description, state=States_for_courier.description)
    dp.register_callback_query_handler(carry_set_date, state=States_for_courier.date)
    dp.register_message_handler(carry_set_price, state=States_for_courier.price)
    dp.register_callback_query_handler(carry_cancel, text=['cancel'], state=States_for_courier.all_states)
