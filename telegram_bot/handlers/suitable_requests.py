from aiogram import types, Dispatcher
from telegram_bot.utils import menu
from telegram_bot.globals import db_name
from telegram_bot.database import find_send_in_base, find_carry_in_base
from telegram_bot.messages import print_suitable_send, print_suitable_carry
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def find_results(callback: types.CallbackQuery):
    send_results = find_send_in_base(db_name, callback.from_user.id)
    carry_results = find_carry_in_base(db_name, callback.from_user.id)

    if len(send_results) != 0:

        await callback.message.answer(
            f'<b>Следующие пользователи хотят отправить свои посылки туда же, куда готовы доставить вы.'
            f'\n\nНапишите им, чтобы договориться о доставке.</b>',
            parse_mode=types.ParseMode.HTML
        )
        for i, x in enumerate(send_results):

            answer_keyboard = InlineKeyboardMarkup(resize_keyboard=True, row=2)
            button_one = InlineKeyboardButton("Вернуться в меню", callback_data='cancel')
            button_two = InlineKeyboardButton("Написать пользователю", url=f'tg://user?id={x[0]}')
            answer_keyboard.add(button_two, button_one)

            await callback.message.answer(
                print_suitable_send(x[4], x[5], x[6], x[7], x[8], x[9], x[1], x[10]),
                parse_mode=types.ParseMode.HTML,
                reply_markup=answer_keyboard
            )

    if len(carry_results) != 0:

        await callback.message.answer(
            f'<b>Следующие пользователи готовы доставить посылки в нужные вам города.'
            f'\n\nНапишите им, чтобы обсудить доставку.</b>',
            parse_mode=types.ParseMode.HTML
        )
        for i, x in enumerate(carry_results):

            answer_keyboard = InlineKeyboardMarkup(resize_keyboard=True, row=2)
            button_one = InlineKeyboardButton("Вернуться в меню", callback_data='cancel')
            button_two = InlineKeyboardButton("Написать пользователю", url=f'tg://user?id={x[0]}')
            answer_keyboard.add(button_two, button_one)

            if x[15] is not None:
                await callback.message.answer(
                    print_suitable_carry(
                        x[4], x[5], x[6], x[7], x[8], x[9], x[1],
                        x[10], x[18], [x[17], x[16], x[15]]
                    ),
                    parse_mode=types.ParseMode.HTML,
                    reply_markup=answer_keyboard
                )
            else:
                await callback.message.answer(
                    print_suitable_carry(
                        x[4], x[5], x[6], x[7], x[8], x[9], x[1],
                        x[10], x[18], False
                    ),
                    parse_mode=types.ParseMode.HTML,
                    reply_markup=answer_keyboard
                )
    if len(send_results) == 0 and len(carry_results) == 0:
        await callback.message.answer(f'Подходящих предложений пока не обнаружено...')


async def base_cancel(callback: types.CallbackQuery):
    await menu(callback.message)


def register_suitable_requests_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(find_results, text=['find_results'])
    dp.register_callback_query_handler(base_cancel, text=['cancel'])
