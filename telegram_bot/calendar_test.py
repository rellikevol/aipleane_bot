import calendar
from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton, ReplyKeyboardMarkup
from datetime import datetime as dt

days_of_week = [
    "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"
]

months = [
    "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
]


def calendar_keyboard(year=dt.today().year.real, month=dt.today().month.real) -> ReplyKeyboardMarkup():
    correct_year = InlineKeyboardButton(str(year), callback_data='calendar_none')
    correct_month = InlineKeyboardButton(months[month - 1], callback_data='calendar_none')
    previous_month = InlineKeyboardButton("<", callback_data='calendar_previous_month')
    next_month = InlineKeyboardButton(">", callback_data='calendar_next_month')
    without_date = InlineKeyboardButton("Не указывать дату", callback_data='without_date')

    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.row(correct_year)
    keyboard.row(previous_month, correct_month, next_month)

    days_names = []
    for day in days_of_week:
        days_names.append(InlineKeyboardButton(f'{day}', callback_data='calendar_none'))

    keyboard.row(*days_names)

    current_calendar = calendar.Calendar().monthdays2calendar(year, month)

    for line in current_calendar:
        days = []
        for day in line:
            if day[0] == 0:
                days.append(
                    InlineKeyboardButton(' ', callback_data='calendar_none')
                )
            else:
                days.append(
                    InlineKeyboardButton(f'{day[0]}', callback_data=f'D_{day[0]}.{month}.{year}')
                )
        keyboard.row(*days)

    keyboard.row(without_date)

    return keyboard
