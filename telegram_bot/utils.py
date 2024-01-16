from telegram_bot.create_bot import bot, storage
from telegram_bot.towns_check import get_town
from aiogram import types
from aiogram.dispatcher import FSMContext
from telegram_bot.keyboards import cancel_menu, town_menu
from telegram_bot.messages import print_address
from telegram_bot.keyboards import basic_menu_one
from telegram_bot.globals import count_of_description


async def menu(message: types.Message):
    await message.answer('Выберите действие:', reply_markup=basic_menu_one)


async def find_town(message: types.Message, state: FSMContext):
    towns = get_town(message.text, 'RU', 10)
    if not towns:
        await message.answer(f'Мы не можем найти такого города. Может попробуете ещё раз?', reply_markup=cancel_menu)
        return False
    else:
        message_id = await bot.send_message(message.chat.id,
                                            print_address(towns[0]['town'], towns[0]['state'], towns[0]['country']),
                                            reply_markup=town_menu,
                                            parse_mode=types.ParseMode.HTML)
        await state.update_data(point_search=towns)
        await state.update_data(point_pos=0)
        await state.update_data(point_len=len(towns))
        await state.update_data(point_message_id=message_id.message_id)
        return True


async def change_town(callback: types.CallbackQuery, state: FSMContext):
    res = await storage.get_data(user=callback.from_user.id)

    index = res['point_pos']

    if index < res['point_len'] - 1:
        index = index + 1

    if index >= res['point_len'] - 1:
        index = 0

    current_point = res['point_search'][index]

    await bot.edit_message_text(print_address(current_point['town'], current_point['state'], current_point['country']),
                                callback.message.chat.id,
                                res['point_message_id'],
                                reply_markup=town_menu,
                                parse_mode=types.ParseMode.HTML)

    await state.update_data(point_pos=index)


async def cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await menu(callback.message)


def count_symbols(txt: str) -> bool:
    if len(txt) <= count_of_description:
        return True
    return False
