import requests

from loader import bot
from telebot.types import Message
from states.hotel_information import HotelInfoState, BestDealState
from utils.api_requests.city_request import city_request
from utils.api_requests.hotels_request import hotels_request
from utils.api_requests.photo_request import photo_request
from time import sleep
from random import choice

is_low_price = None
is_best_deal = None
tmp_min_price = 0


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def any_command(message: Message) -> None:
    global is_low_price, is_best_deal
    if message.text[1:] == 'lowprice':
        is_low_price, is_best_deal = True, False

    elif message.text[1:] == 'bestdeal':
        is_best_deal, is_low_price = True, False

    else:
        is_low_price, is_best_deal = False, False

    bot.set_state(message.from_user.id, HotelInfoState.city, message.chat.id)
    bot.send_message(message.from_user.id, choice(['Введите название города',
                                                   'Где будем искать?',
                                                   'Какой город выбрали для поиска?',
                                                   'В каком городе будем искать?',
                                                   'Введите город для поиска']))


@bot.message_handler(state=HotelInfoState.city)
def get_city(message: Message) -> None:

    if message.text.isalpha() and city_request(message.text):
        bot.set_state(message.from_user.id, HotelInfoState.hotel_amt, message.chat.id)
        sleep(2)
        bot.send_message(message.from_user.id, choice(['Отлично! Теперь введите количество отелей',
                                                       'Прекрасно! Теперь мне нужно количество отелей',
                                                       'Замечательно! Сколько отелей ищем?']))

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'], data['cityID'] = city_request(message.text)
    else:
        bot.send_message(message.from_user.id, choice(['Не нашел такого города.\n'
                                                       'Попробуйте еще раз',
                                                       'Что-то не могу найти такой город.\n'
                                                       'Попробуйте еще раз',
                                                       'Странно... Нет информации по такому городу.\n'
                                                       'Попробуйте еще раз']))


@bot.message_handler(state=HotelInfoState.hotel_amt)
def get_hotel_amt(message: Message) -> None:

    if message.text.isdigit() and 0 < int(message.text) <= 10:
        bot.set_state(message.from_user.id, HotelInfoState.need_photo, message.chat.id)
        sleep(2)
        bot.send_message(message.from_user.id, choice(['Отлично! Нужны ли фотографии?',
                                                       'Замечательно! Фотографии будем искать?',
                                                       'Очень хорошо! Нужны фотографии?']))

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotel_amt'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, choice(['Количество должно быть положительным числом '
                                                       'и я смогу обработать '
                                                       'не больше 10 отелей',
                                                       'Моих сил хватит на 10 отелей и тут жду число...\n'
                                                       'Положительное...',
                                                       'Нужно ввести число, которое больше 0 и меньше 11']))


@bot.message_handler(state=HotelInfoState.need_photo)
def get_photos(message: Message) -> None:
    if message.text == 'Да':

        bot.set_state(message.from_user.id, HotelInfoState.photo_amt, message.chat.id)
        bot.send_message(message.from_user.id, choice(['Значит с фотографиями.\n'
                                                       'Введите количество фотографий',
                                                       'Хорошо, будут фотографии.📸\n'
                                                       'Пойду нафоткаю😆\n'
                                                       'Сколько фотографий на отель?',
                                                       'Отметил у себя в блокноте.\n'
                                                       'Фотографии нужны ✅\n'
                                                       'Запишу - какое количество фотографий?']))
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = True

    elif message.text == 'Нет':
        bot.set_state(message.from_user.id, HotelInfoState.info_low_high, message.chat.id)

        if not is_best_deal:
            bot.send_message(message.from_user.id, choice(['Вывести информацию по запросу?',
                                                           'Так...\nВыводим информацию по запросу?',
                                                           'Нужна информация по запросу?\n'
                                                           'Принимаю только "Да"🤫']))
        else:
            bot.send_message(message.from_user.id, choice(['Продолжаем?',
                                                           'Идем дальше?',
                                                           'Вы тут?🥶',
                                                           'Ау🔎, пойдем дальше искать?']))

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['need_photo'] = False

    else:
        bot.send_message(message.from_user.id, choice(['Так "Да" или "Нет"?',
                                                       '🔙 Нужно "Нет" либо "Да"',
                                                       '📴 "Да" или "Нет"',
                                                       '🤦 Пойму только "Да" или "Нет"']))


@bot.message_handler(state=HotelInfoState.photo_amt)
def photo_amt(message: Message) -> None:
    if message.text.isdigit() and 0 < int(message.text) <= 5:
        bot.set_state(message.from_user.id, HotelInfoState.info_low_high, message.chat.id)
        if not is_best_deal:
            bot.send_message(message.from_user.id, choice(['Прекрасно!\n'
                                                           'Выводим информацию по запросу?📑',
                                                           'Успешно!\n'
                                                           'Вывести информацию по запросу?📜',
                                                           'Готово!\n'
                                                           'Нужна информация по запросу?📃']))
        else:
            bot.send_message(message.from_user.id, choice(['Превосходно!\n'
                                                           'Продолжаем, чтобы подобрать лучшие варианты?🏩',
                                                           'Отличненько!\n'
                                                           'Подбираем дальше лучшие предложения?🏨',
                                                           'Отлично!\n'
                                                           'Идем дальше, искать лучшие отели?🏨']))

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_amt'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, choice(['Я смогу обработать только 5 фотографий\n'
                                                       'И убедитесь, что вводите число',
                                                       'Тут такое дело...\n'
                                                       'Мой процессор вытянет только 5 фотографий\n'
                                                       'И только положительное число',
                                                       'Всё, что между 0 и 5(включительно) я приму😊']))


@bot.message_handler(state=HotelInfoState.info_low_high)
def info_low_high(message: Message) -> None:

    if message.text == 'Да':
        if is_best_deal:
            bot.set_state(message.from_user.id, BestDealState.price_min, message.chat.id)
            bot.send_message(message.from_user.id, choice(['Введите минимальную цену для поиска($)',
                                                           'Нужна минимальная цена для поиска ($)',
                                                           'Пожалуйста, введите минимальную цену для поиска ($)']))
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

                if data['need_photo']:
                    full_info = f"Чудесно!\nВаш запрос:\n" \
                                f"Город: {data['city']}\n" \
                                f"ID города: {data['cityID']}\n" \
                                f"Количество отелей: {data['hotel_amt']}\n" \
                                f"Количество фотографий: {data['photo_amt']}"
                else:
                    full_info = f"Отлично!\nВаш запрос:\n" \
                                f"Город: {data['city']}\n" \
                                f"ID города: {data['cityID']}\n" \
                                f"Количество отелей: {data['hotel_amt']}\n" \
                                f"Без фотографий"

            bot.send_message(message.from_user.id, full_info)
            bot.send_message(message.from_user.id, choice(['Ожидайте...',
                                                           'Можно 💤? Ждём...',
                                                           'Тик-так ⌛ Ожидаем...',
                                                           'Надеюсь моя 🔋 не сядет...\n'
                                                           'Шучу😉 Просто чуток подождем...',
                                                           'Возьмите пока что 🎧\n'
                                                           'И немного подождем...']))

            low_to_high = "PRICE_LOW_TO_HIGH"
            high_to_low = "PRICE_HIGH_TO_LOW"

            if is_low_price:
                sorting = low_to_high
            else:
                sorting = high_to_low

            offers = hotels_request(data['cityID'], data['hotel_amt'], sorting)

            if offers and not data['need_photo']:

                if sorting == "PRICE_LOW_TO_HIGH":
                    sort_val = sorted(offers.items(), key=lambda val: int(val[1][1][1:]))
                else:
                    sort_val = sorted(offers.items(), key=lambda val: int(val[1][1][1:]), reverse=True)

                bot.send_message(message.from_user.id, choice(['Подобраны следующие варианты:',
                                                               'Что удалось подобрать:',
                                                               'Подобрал следующее:']))
                count = 1

                for i_info in sort_val:
                    bot.send_message(message.from_user.id,
                                     f'{count}. <b>{i_info[1][0]}</b>\n'
                                     f'<i>Цена: {i_info[1][1]}</i>',
                                     parse_mode='html')
                    count += 1

            elif offers and data['need_photo']:
                sort_offers = sorted(offers.items(), key=lambda val: int(val[1][1][1:]))
                bot.send_message(message.from_user.id, choice(['Подобраны следующие варианты:',
                                                               'Что удалось подобрать:',
                                                               'Подобрал следующее:']))
                count = 1

                for i_offer in sort_offers:
                    offer_with_photo = photo_request(i_offer[0], data['photo_amt'])
                    bot.send_message(message.from_user.id,
                                     f'{count}. <b>{i_offer[1][0]}</b>\n'
                                     f'<i>Цена: {i_offer[1][1]}</i>',
                                     parse_mode='html')
                    count += 1

                    for i_name, i_lst in offer_with_photo.items():
                        for i_dct in i_lst:
                            for i_url, i_desc in i_dct.items():
                                photo_file = requests.get(i_url)
                                bot.send_photo(message.from_user.id, photo_file.url, message.chat.id)
                                bot.send_message(message.from_user.id, f'{i_desc}')
            else:
                bot.send_message(message.from_user.id, choice(['Произошла какая-то ошибка на сервере.\n'
                                                               'Попробуйте выбрать другой город',
                                                               'Что-то пошло не так...\n'
                                                               'Попробуйте выбрать другой город',
                                                               'Что-то случилось на сервере\n'
                                                               'Выберите другой город']))

    else:
        bot.send_message(message.from_user.id, choice(['Скажите же мне "Да"',
                                                       'Ну прошу вас 🙏\n'
                                                       'Введите "Да"',
                                                       'Так хочется поделиться информацией😩\n'
                                                       'Жду ваше "Да"',
                                                       '"Да"🥱']))


@bot.message_handler(state=BestDealState.price_min)
def price_min_for_best_deal(message: Message) -> None:

    global tmp_min_price
    if message.text.isdigit() and int(message.text) > 0:
        tmp_min_price = int(message.text)
        bot.set_state(message.from_user.id, BestDealState.price_max, message.chat.id)
        bot.send_message(message.from_user.id, choice(['Теперь введите максимальную цену {$}',
                                                       'А сейчас нужна максимальная цена для поиска ($)',
                                                       'Теперь необходима максимальная цена для поиска ($)']))
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_min'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, choice(['Цена должна быть числом, причём положительным...\n'
                                                       'Попробуйте снова',
                                                       'Минимальная цена - это положительное число\n'
                                                       'Попробуйте еще раз',
                                                       'Не понимаю этих символов...'
                                                       'Попробуйте ввести положительное число']))


@bot.message_handler(state=BestDealState.price_max)
def price_max_for_best_deal(message: Message) -> None:

    global tmp_min_price
    if message.text.isdigit() and int(message.text) > tmp_min_price:
        bot.set_state(message.from_user.id, BestDealState.distance, message.chat.id)
        bot.send_message(message.from_user.id, choice(['А теперь введите расстояние до центра города (км)',
                                                       'Теперь мне нужно знать -\n'
                                                       'Какое расстояние до центра вас устроит (км)',
                                                       'Теперь нужно ввести расстояние до центра города (км)']))

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price_max'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, 'Цена должна быть положительным числом?\n'
                                               'А также проверьте🧐 -\n'
                                               'Не является ли максимальная цена меньше минимальной\n'
                                               'Попробуйте снова')


@bot.message_handler(state=BestDealState.distance)
def distance(message: Message) -> None:
    if message.text.isdigit() and int(message.text) > 0:
        bot.set_state(message.from_user.id, BestDealState.info_best_deal)
        bot.send_message(message.from_user.id, choice(['Классно, расстояние у нас есть!\n'
                                                       'Выводим информацию по запросу?',
                                                       'Успешно отметил расстояние!\n'
                                                       'Вывести информацию по запросу?',
                                                       'Отлично, расстояние получено!\n'
                                                       'Отобразить информацию по запросу?']))

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance'] = int(message.text)
    else:
        bot.send_message(message.from_user.id, choice(['Приму только число и только положительное...',
                                                       'Расстояние - это положительное число',
                                                       'Попробуйте ввести положительное число']))


@bot.message_handler(state=BestDealState.info_best_deal)
def info_best_deal(message: Message) -> None:
    if message.text == 'Да':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if data['need_photo']:
                full_info = f"Замечательно!\nВаш запрос:\n" \
                            f"Город: {data['city']}\n" \
                            f"ID города: {data['cityID']}\n" \
                            f"Количество отелей: {data['hotel_amt']}\n" \
                            f"Количество фотографий: {data['photo_amt']}\n" \
                            f"Минимальная цена: {data['price_min']}\n" \
                            f"Максимальная цена: {data['price_max']}\n" \
                            f"Расстояние до центра: {data['distance']}"

            else:
                full_info = f"Превосходно!\nВаш запрос:\n" \
                            f"Город: {data['city']}\n" \
                            f"ID города: {data['cityID']}\n" \
                            f"Количество отелей: {data['hotel_amt']}\n" \
                            f"Без фотографий\n" \
                            f"Минимальная цена: {data['price_min']}\n" \
                            f"Максимальная цена: {data['price_max']}\n" \
                            f"Расстояние до центра: {data['distance']}"

            bot.send_message(message.from_user.id, full_info)
            bot.send_message(message.from_user.id, choice(['Ожидайте...',
                                                           'Можно 💤? Ждём...',
                                                           'Тик-так ⌛ Ожидаем...',
                                                           'Надеюсь моя 🔋 не сядет...\n'
                                                           'Шучу😉 Просто чуток подождем...',
                                                           'Возьмите пока что 🎧\n'
                                                           'И немного подождем...']))

            offers = hotels_request(data['cityID'],
                                    data['hotel_amt'],
                                    'DISTANCE',
                                    price_min=data['price_min'],
                                    price_max=data['price_max'],
                                    distance=data['distance'])

            sort_offers = sorted(offers.items(), key=lambda val: int(val[1][1][1:]))

            if offers and not data['need_photo']:
                bot.send_message(message.from_user.id, choice(['Подобраны следующие варианты:',
                                                               'Что удалось подобрать:',
                                                               'Подобрал следующее:']))

                count = 1

                for i_info in sort_offers:
                    bot.send_message(message.from_user.id,
                                     f'{count}. <b>{i_info[1][0]}</b>\n'
                                     f'<i>Цена: {i_info[1][1]}</i>\n'
                                     f'<i>Расстояние до центра: {i_info[1][2]} км</i>',
                                     parse_mode='html')
                    count += 1

            elif offers and data['need_photo']:
                count = 1

                for i_offer in sort_offers:
                    offer_with_photo = photo_request(i_offer[0], data['photo_amt'])
                    bot.send_message(message.from_user.id,
                                     f'{count}. <b>{i_offer[1][0]}</b>\n'
                                     f'<i>Цена: {i_offer[1][1]}</i>\n'
                                     f'<i>Расстояние до центра: {i_offer[1][2]} км</i>',
                                     parse_mode='html')
                    count += 1

                    for i_name, i_lst in offer_with_photo.items():
                        for i_dct in i_lst:
                            for i_url, i_desc in i_dct.items():
                                photo_file = requests.get(i_url)
                                bot.send_photo(message.from_user.id, photo_file.url, message.chat.id)
                                bot.send_message(message.from_user.id, f'{i_desc}')
            else:
                bot.send_message(message.from_user.id, 'К сожалению, не нашел подходящих вариантов😔\n'
                                                       'Либо произошла какая-то ошибка на сервере⚠\n'
                                                       'Попробуйте выбрать другой город')
    else:
        bot.send_message(message.from_user.id, choice(['Скажите же мне "Да"',
                                                       'Ну прошу вас 🙏\n'
                                                       'Введите "Да"',
                                                       'Так хочется поделиться информацией😩\n'
                                                       'Жду ваше "Да"',
                                                       '"Да"🥱',
                                                       'Я так хочу поделиться информацией...\n'
                                                       'А у меня 🤐\n'
                                                       'Напишите "Да"']))
