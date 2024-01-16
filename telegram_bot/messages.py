from datetime import date


def message_for_devs() -> str:
    return f"Возникли вопросы или пожелания по работе бота?\n\n" \
           f"Опишите их здесь, разработчики постараются отреагировать в ближайшее время."

def print_address(town: str, state: str, country: str) -> str:
    return f"<i>Это верный адрес?</i>\n\n" \
           f"<b>Город: </b> {town}\n" \
           f"<b>Субьект: </b> {state}\n" \
           f"<b>Страна: </b> {country}\n"


def print_suitable_send_request(point_from_town: str, point_from_state: str, point_from_country: str,
                                point_to_town: str, point_to_state: str, point_to_country: str,
                                username: str, description: str) -> str:
    return f"<i>По вашему запросу появилась подходящая заявка:</i>\n\n"\
           f"Напишите этому пользователю чтобы договориться доставке.\n\n" \
           f"<b>Тип:</b> хочу отправить\n" \
           f"<b>Откуда:</b> {point_from_town}, {point_from_state}, {point_from_country}\n" \
           f"<b>Куда:</b> {point_to_town}, {point_to_state}, {point_to_country}\n" \
           f"<b>Описание:</b> {description}\n"

def print_suitable_send(point_from_town: str, point_from_state: str, point_from_country: str,
                        point_to_town: str, point_to_state: str, point_to_country: str,
                        username: str, description: str) -> str:
    return f"<b>Тип:</b> хочу отправить\n" \
           f"<b>Откуда:</b> {point_from_town}, {point_from_state}, {point_from_country}\n" \
           f"<b>Куда:</b> {point_to_town}, {point_to_state}, {point_to_country}\n" \
           f"<b>Описание:</b> {description}\n"


def print_suitable_carry_request(point_from_town: str, point_from_state: str, point_from_country: str,
                                 point_to_town: str, point_to_state: str, point_to_country: str,
                                 username: str, description: str, price: str, date_one) -> str:
    result = f"<i>По вашему запросу появилась подходящая заявка!</i>\n\n" \
             f"Напишите этому пользователю чтобы договориться доставке.\n\n" \
             f"<b>Тип:</b> могу отвезти\n" \
             f"<b>Откуда:</b> {point_from_town}, {point_from_state}, {point_from_country}\n" \
             f"<b>Куда:</b> {point_to_town}, {point_to_state}, {point_to_country}\n" \
             f"<b>Описание:</b> {description}\n" \
             f"<b>Стоимость:</b> {price}"
    if date_one:
        date_two = date(date_one[2], date_one[1], date_one[0])
        return result + f"\n <b>Дата:</b> {date_two.strftime('%d.%m.%Y')}"
    else:
        return result


def print_suitable_carry(point_from_town: str, point_from_state: str, point_from_country: str,
                         point_to_town: str, point_to_state: str, point_to_country: str,
                         username: str, description: str, price: str, date_one) -> str:
    result = f"<b>Тип:</b> могу отвезти\n" \
             f"<b>Откуда:</b> {point_from_town}, {point_from_state}, {point_from_country}\n" \
             f"<b>Куда:</b> {point_to_town}, {point_to_state}, {point_to_country}\n" \
             f"<b>Описание:</b> {description}\n" \
             f"<b>Стоимость:</b> {price}"
    if date_one:
        date_two = date(date_one[2], date_one[1], date_one[0])
        return result + f"\n <b>Дата:</b> {date_two.strftime('%d.%m.%Y')}"
    else:
        return result


def send_request_are_registered():
    return f"<b>Заявка на отправку посылки зарегистрирована!</b>\n\n" \
           f"Мы сообщим вам, как только появится подходящее предложение по тоставке.\n"


def carry_request_are_registered():
    return f"<b>Предложение по доставке посылки зарегистрировано!</b>\n\n" \
           f"Мы сообщим вам, как только появится подходящая заявка на отправку.\n"

def about() -> str:
    return f''