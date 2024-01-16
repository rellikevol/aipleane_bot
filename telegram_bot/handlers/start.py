from aiogram import types, Dispatcher
from telegram_bot.utils import menu


async def start(message: types.Message):
    await message.answer(f'Здравствуйте, {message.chat.full_name}!')
    await menu(message)


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
