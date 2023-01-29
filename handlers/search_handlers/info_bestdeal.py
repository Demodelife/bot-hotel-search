import requests
from loader import bot
from telebot.types import Message
from states.hotel_information import BestDealState
from utils.api_requests.hotels_request import hotels_request
from utils.api_requests.photo_request import photo_request
from random import choice


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
                            f"Минимальная цена: {data['price_min']}$\n" \
                            f"Максимальная цена: {data['price_max']}$\n" \
                            f"Расстояние до центра: {data['distance']} км"

            else:
                full_info = f"Превосходно!\nВаш запрос:\n" \
                            f"Город: {data['city']}\n" \
                            f"ID города: {data['cityID']}\n" \
                            f"Количество отелей: {data['hotel_amt']}\n" \
                            f"Без фотографий\n" \
                            f"Минимальная цена: {data['price_min']}$\n" \
                            f"Максимальная цена: {data['price_max']}$\n" \
                            f"Расстояние до центра: {data['distance']} км"

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
                                bot.send_photo(message.from_user.id,
                                               photo_file.url,
                                               caption=f'{i_desc}')
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
