from aiogram import types, Dispatcher
from telegram_bot.utils import menu
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot.globals import db_name
from telegram_bot.keyboards import delete_menu
from telegram_bot.utils import cancel
from telegram_bot.create_bot import storage
from telegram_bot.database import user_tasks_send, user_tasks_carry, get_request, delete_request
from telegram_bot.messages import print_suitable_send, print_suitable_carry


class States_for_delete(StatesGroup):
    delete_request = State()
    delete_final = State()


# ---------------------- my requests--------------------------------------

async def send_tasks(callback: types.CallbackQuery):
    res = user_tasks_send(db_name, callback.from_user.id)

    if res:
        for i, x in enumerate(res):
            button = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
            button.add(
                InlineKeyboardButton("Удалить", callback_data=f'{x[19]}'),
                InlineKeyboardButton("Вернуться в меню", callback_data='cancel')
            )
            await callback.message.answer(
                print_suitable_send(x[4], x[5], x[6], x[7], x[8], x[9], x[1], x[10]),
                parse_mode=types.ParseMode.HTML,
                reply_markup=button)
        await States_for_delete.delete_request.set()
        await callback.message.answer(f'Здесь вы можете отредактировать размещённые вами предложения.')
    else:
        await callback.message.answer(f'Вы пока не создали ни одной заявки на отправку.')


async def carry_tasks(callback: types.CallbackQuery):
    res = user_tasks_carry(db_name, callback.from_user.id)

    if res:
        for i, x in enumerate(res):
            button = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
            button.add(
                InlineKeyboardButton("Удалить", callback_data=f'{x[19]}'),
                InlineKeyboardButton("Вернуться в меню", callback_data='cancel')
            )
            await callback.message.answer(
                print_suitable_carry(
                    x[4], x[5], x[6],
                    x[7], x[8], x[9],
                    x[1], x[10],
                    x[18],
                    [x[17], x[16], x[15]]
                ),
                parse_mode=types.ParseMode.HTML,
                reply_markup=button)
        await States_for_delete.delete_request.set()
        await callback.message.answer(f'Здесь вы можете отредактировать размещённые вами предложения.')
    else:
        await callback.message.answer(f'Вы пока не создали ни одного предложения на доставку.')


# ------------------------ delete ----------------------------------

async def delete_cancel(callback: types.CallbackQuery, state: FSMContext):
    await cancel(callback, state)


async def delete_requests(callback: types.CallbackQuery, state: FSMContext):
    pk = callback.data
    x = get_request(db_name, pk)[0]
    if not x:
        await callback.message.answer('Эта запись уже удалена...')
    else:
        await state.update_data(delete_request=pk)
        await callback.message.answer('<b>Вы уверены что хотите удалить эту запись?</b>',
                                      parse_mode=types.ParseMode.HTML)
        if x[3] == 'send':
            await callback.message.answer(print_suitable_send(x[4], x[5], x[6], x[7], x[8], x[9],
                                                              x[1], x[10]), parse_mode=types.ParseMode.HTML,
                                          reply_markup=delete_menu)
        if x[3] == 'carry':
            if x[15] is not None:
                await callback.message.answer(print_suitable_carry(x[4], x[5], x[6], x[7], x[8], x[9], x[1],
                                                                   x[10], x[18], [x[17], x[16], x[15]]),
                                              parse_mode=types.ParseMode.HTML, reply_markup=delete_menu)
            else:
                await callback.message.answer(print_suitable_carry(x[4], x[5], x[6], x[7], x[8], x[9], x[1],
                                                                   x[10], x[18], False),
                                              parse_mode=types.ParseMode.HTML, reply_markup=delete_menu)
        await States_for_delete.delete_final.set()


async def delete_requests_final(callback: types.CallbackQuery, state: FSMContext):
    res = await storage.get_data(user=callback.from_user.id)
    pk = res['delete_request']
    delete_request(db_name, pk)
    await callback.answer(f'Запись успешно удалена.')
    await state.finish()
    await menu(callback.message)


async def delete_requests_cancel(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(f'Отмена.')
    await state.finish()
    await menu(callback.message)


# --------------------------------------------

def register_my_requests_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(send_tasks, text=['my_requests_send'])
    dp.register_callback_query_handler(carry_tasks, text=['my_requests_carry'])
    dp.register_callback_query_handler(delete_cancel, text=['cancel'], state=States_for_delete.all_states)
    dp.register_callback_query_handler(delete_requests, state=States_for_delete.delete_request)
    dp.register_callback_query_handler(delete_requests_final, text=['delete_yes'], state=States_for_delete.delete_final)
    dp.register_callback_query_handler(delete_requests_cancel, text=['delete_no'], state=States_for_delete.delete_final)
