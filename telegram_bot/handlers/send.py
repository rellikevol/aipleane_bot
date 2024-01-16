from aiogram import types, Dispatcher
from telegram_bot.utils import menu
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from telegram_bot.globals import db_name, count_of_description
from telegram_bot.keyboards import cancel_menu
from telegram_bot.utils import cancel, count_symbols
from telegram_bot.utils import find_town, change_town
from telegram_bot.create_bot import storage, bot
from telegram_bot.database import insert_send, find_carry_while_create
from telegram_bot.messages import print_suitable_send_request, send_request_are_registered
from datetime import datetime as dt
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class States_for_sender(StatesGroup):
    point_search = State()
    point_pos = State()
    point_len = State()
    point_message_id = State()
    point_from = State()
    point_to = State()
    description = State()


# ------------- create send request ------------------------------------------


async def send(callback: types.CallbackQuery):
    await callback.message.answer(f'Укажите город из которого хотите отправить посылку:', reply_markup=cancel_menu)
    await States_for_sender.point_search.set()


async def send_set_from_search(message: types.Message, state: FSMContext):
    if await find_town(message, state):
        res = await storage.get_data(user=message.from_user.id)
        if 'point_from' in res:
            await States_for_sender.point_to.set()
        else:
            await States_for_sender.point_from.set()


# --------------- point from ----------------------

async def town_from_check(callback: types.CallbackQuery, state: FSMContext):
    await change_town(callback, state)


async def town_from_set(callback: types.CallbackQuery, state: FSMContext):
    res = await storage.get_data(user=callback.from_user.id)
    await state.update_data(point_from=res['point_search'][res['point_pos']])
    await callback.message.answer(f'Укажите город, в который вы хотели бы отправить:', reply_markup=cancel_menu)
    await States_for_sender.point_search.set()


# ----------------------------- point to --------------------

async def town_to_check(callback: types.CallbackQuery, state: FSMContext):
    await change_town(callback, state)


async def town_to_set(callback: types.CallbackQuery, state: FSMContext):
    res = await storage.get_data(user=callback.from_user.id)
    await state.update_data(point_to=res['point_search'][res['point_pos']])
    await callback.message.answer(f'Опишите, что вы хотите отправить? '
                                  f'<i>(не более {count_of_description} символов)</i>', reply_markup=cancel_menu,
                                  parse_mode=types.ParseMode.HTML)
    await States_for_sender.description.set()


# ------------ sender description --------------------------

async def send_set_description(message: types.Message, state: FSMContext):
    if count_symbols(message.text):
        await state.update_data(description=message.text)
        res = await storage.get_data(user=message.from_user.id)
        insert_send(db_name, message.from_user.id, message.from_user.username, message.chat.id, "send",
                    res['point_from']['town'], res['point_from']['state'], res['point_from']['country'],
                    res['point_to']['town'], res['point_to']['state'], res['point_to']['country'],
                    res['description'], 'created', dt.now().year, dt.now().month, dt.now().day)

        carry_one = find_carry_while_create(
            db_name,
            res['point_from']['town'], res['point_from']['state'],
            res['point_from']['country'],
            res['point_to']['town'], res['point_to']['state'], res['point_to']['country']
        )

        if len(carry_one) != 0:

            for i in carry_one:
                if i != message.from_user.id:
                    answer_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
                    button_two = InlineKeyboardButton("Написать пользователю",
                                                      url=f'tg://user?id={message.from_user.id}')
                    answer_keyboard.add(button_two)

                    await bot.send_message(
                        i,
                        print_suitable_send_request(
                            res['point_from']['town'], res['point_from']['state'], res['point_from']['country'],
                            res['point_to']['town'], res['point_to']['state'], res['point_to']['country'],
                            message.from_user.username, res['description']
                        ),
                        parse_mode=types.ParseMode.HTML,
                        reply_markup=answer_keyboard
                    )

        await message.answer(send_request_are_registered(), parse_mode=types.ParseMode.HTML)
        # ------------ добавить сообщение с подходящей заявкой ---------------------------------------------
        await state.finish()
        await menu(message)
    else:
        await message.answer(
            f'Это описание слишком длинное, попробуйте описать короче... '
            f'<i>(не более {count_of_description} символов)</i>',
            reply_markup=cancel_menu,
            parse_mode=types.ParseMode.HTML
        )


async def send_cancel(callback: types.CallbackQuery, state: FSMContext):
    await cancel(callback, state)


def register_create_send_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(send, text=['create_request'])
    dp.register_message_handler(send_set_from_search, state=States_for_sender.point_search)
    dp.register_callback_query_handler(town_from_check, text=['town_no'], state=States_for_sender.point_from)
    dp.register_callback_query_handler(town_from_set, text=['town_yes'], state=States_for_sender.point_from)
    dp.register_callback_query_handler(town_to_check, text=['town_no'], state=States_for_sender.point_to)
    dp.register_callback_query_handler(town_to_set, text=['town_yes'], state=States_for_sender.point_to)
    dp.register_message_handler(send_set_description, state=States_for_sender.description)
    dp.register_callback_query_handler(send_cancel, text=['cancel'], state=States_for_sender.all_states)
