from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from telegram_bot.messages import message_for_devs
from telegram_bot.database import insert_devs_message
from telegram_bot.globals import db_name
from telegram_bot.keyboards import cancel_menu
from telegram_bot.utils import cancel
from telegram_bot.utils import menu


class States_for_devs(StatesGroup):
    devs_message = State()


async def devs_set(callback: types.CallbackQuery):
    await callback.message.answer(message_for_devs(), parse_mode=types.ParseMode.HTML, reply_markup=cancel_menu)
    await States_for_devs.devs_message.set()


async def devs_set_two(message: types.Message, state: FSMContext):
    insert_devs_message(db_name, message.from_user.id, message.from_user.username, message.text)
    await message.answer(f"Сообщение отправлено.")
    await state.finish()
    await menu(message)


async def devs_cancel(callback: types.CallbackQuery, state: FSMContext):
    await cancel(callback, state)


def register_message_for_devs_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(devs_set, text=['send_message_to_devs'])
    dp.register_message_handler(devs_set_two, state=States_for_devs.devs_message)
    dp.register_callback_query_handler(devs_cancel, text=['cancel'], state=States_for_devs.all_states)
