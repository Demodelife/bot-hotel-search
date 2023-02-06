from loader import bot
from states.contact_information import UserInfoState
from telebot.types import Message
from keyboards.reply.contact import request_contact
from datetime import datetime
from loguru import logger
from database.hotels_db import PersonSurvey
from telebot.types import ReplyKeyboardRemove


@bot.message_handler(commands=['survey'])
def survey(message: Message) -> None:
    """Хэндлер команды /survey, опросника"""

    bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
    bot.send_message(message.from_user.id, f'Приветствую тебя в опроснике, {message.from_user.username}! '
                                           f'Введи свое имя')


@bot.message_handler(state=UserInfoState.name)
def get_name(message: Message) -> None:
    """Хэндлер состояния имени"""

    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Отлично, записал! Теперь можешь ввести свой возраст')
        bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['name'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Какое странное у тебя имя...🤔'
                                               'Может проверишь - нет ли там цифр...')


@bot.message_handler(state=UserInfoState.age)
def get_age(message: Message) -> None:
    """Хэндлер состояния возраста"""

    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Отлично, записал! '
                                               'Теперь можешь ввести страну проживания')
        bot.set_state(message.from_user.id, UserInfoState.country, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['age'] = message.text

    else:
        bot.send_message(message.from_user.id, 'Возраст вообще-то состоит из цифр...🤔')


@bot.message_handler(state=UserInfoState.country)
def get_country(message: Message) -> None:
    """Хэндлер состояния страны"""

    bot.send_message(message.from_user.id, 'Отлично, записал! '
                                           'Теперь можешь ввести свой город')
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['country'] = message.text


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    """Хэндлер состояния города"""

    bot.send_message(message.from_user.id,
                     'Отлично, записал!\n'
                     'Отправь свой номер нажав на кнопку или откажитесь отправив "Нет"',
                     reply_markup=request_contact())
    bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text


@logger.catch
@bot.message_handler(content_types=['text', 'contact'], state=UserInfoState.phone_number)
def get_contact(message: Message) -> None:
    """Хэндлер состояния номера телефона"""

    if message.content_type == 'contact':

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number

        full_info = 'Спасибо за прохождение опроса! Ваши данные:\n' \
                    f'Имя: {data["name"]}\n' \
                    f'Возраст: {data["age"]}\n' \
                    f'Страна: {data["country"]}\n' \
                    f'Город: {data["city"]}\n' \
                    f'Номер телефона: {data["phone_number"]}'

        bot.send_message(message.from_user.id, full_info, reply_markup=ReplyKeyboardRemove())
        PersonSurvey.create(date=datetime.now().strftime('%d-%b-%Y %H:%M:%S'),
                            userID=message.from_user.id,
                            name=data['name'],
                            age=data['age'],
                            country=data['country'],
                            city=data['city'],
                            phone_number=data['phone_number'])
        bot.delete_state(message.from_user.id, message.chat.id)
    elif message.text == 'Нет':

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.text

        full_info = 'Спасибо за прохождение опроса! Ваши данные:\n' \
                    f'Имя: {data["name"]}\n' \
                    f'Возраст: {data["age"]}\n' \
                    f'Страна: {data["country"]}\n' \
                    f'Город: {data["city"]}\n' \
                    f'Номер телефона: {data["phone_number"]}'

        bot.send_message(message.from_user.id, full_info, reply_markup=ReplyKeyboardRemove())
        PersonSurvey.create(date=datetime.now().strftime('%d-%b-%Y %H:%M:%S'),
                            userID=message.from_user.id,
                            name=data['name'],
                            age=data['age'],
                            country=data['country'],
                            city=data['city'])
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Чтобы отправить контактную информацию,\n'
                                               'нажми на кнопку "Отправить контакт"\n'
                                               'Или напишите "Нет"')
