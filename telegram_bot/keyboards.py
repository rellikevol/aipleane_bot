from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup


create_send_one = InlineKeyboardButton("Хочу отправить посылку", callback_data='create_request')
create_carry_one = InlineKeyboardButton("Могу взять посылку с собой", callback_data='create_carry')
my_requests_one_send = InlineKeyboardButton("Мои заявки: хочу отправить", callback_data='my_requests_send')
my_requests_one_carry = InlineKeyboardButton("Мои заявки: могу отвезти", callback_data='my_requests_carry')
find_results_one = InlineKeyboardButton("Подходящие заявки", callback_data='find_results')
send_message_to_devs = InlineKeyboardButton("Написать разработчикам", callback_data='send_message_to_devs')
basic_menu_one = InlineKeyboardMarkup(resize_keyboard=True)
basic_menu_one.row(create_send_one, create_carry_one)
basic_menu_one.row(my_requests_one_send, my_requests_one_carry)
basic_menu_one.row(find_results_one)
basic_menu_one.row(send_message_to_devs)


create_send_two = KeyboardButton("Отправить посылку")
create_carry_two = KeyboardButton("Отвезти посылку")
my_requests_two = KeyboardButton("Мои заявки")
find_request_two = KeyboardButton("Найти подходящие")
basic_menu_two = ReplyKeyboardMarkup(resize_keyboard=True)
basic_menu_two.add(create_send_two, create_carry_two, find_request_two, my_requests_two)

cancel = InlineKeyboardButton("Отмена", callback_data='cancel')
cancel_menu = InlineKeyboardMarkup(resize_keyboard=True)
cancel_menu.add(cancel)

town_yes = InlineKeyboardButton("Да", callback_data='town_yes')
town_no = InlineKeyboardButton("Другой вариант >>>", callback_data='town_no')
town_menu = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
town_menu.add(town_yes, town_no, cancel)

without_date = InlineKeyboardButton("Не указывать дату", callback_data='without_date')
without_date_keyboard = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
without_date_keyboard.add(without_date, cancel)

delete_yes = InlineKeyboardButton("Да", callback_data='delete_yes')
delete_no = InlineKeyboardButton("Нет", callback_data='delete_no')
delete_menu = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
delete_menu.add(delete_yes, delete_no)