import requests
from loader import bot
from telebot.types import Union, CallbackQuery, Message
from states.hotel_information import HotelInfoState, BestDealState
from utils.api_requests.hotels_request import post_hotels_request
from utils.api_requests.detail_request import post_detail_request
from random import choice
from . import base_commands
from keyboards.inline.all_keyboards import row_address_and_on_map
from loguru import logger


@logger.catch
@bot.message_handler(state=HotelInfoState.info_low_high)
def info_low_high(message: Union[CallbackQuery, Message]) -> None:

    if message.text == 'Да':
        if base_commands.is_best_deal:
            bot.set_state(message.from_user.id, BestDealState.price_min, message.chat.id)
            bot.send_message(message.from_user.id, choice(['Введите минимальную цену для поиска($)',
                                                           'Нужна минимальная цена для поиска ($)',
                                                           'Пожалуйста, введите минимальную цену для поиска ($)']))
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

                if data['need_photo']:

                    full_info = f"Чудесно!\nВаш запрос:\n" \
                                f'<b>"Самые {base_commands.cost_var} отели в городе"</b>\n' \
                                f"Город: {data['city']}\n" \
                                f"Количество отелей: {data['hotel_amt']}\n" \
                                f"Количество фотографий: {data['photo_amt']}"
                else:
                    full_info = f"Отлично!\nВаш запрос:\n" \
                                f'<b>"Самые {base_commands.cost_var} отели в городе"</b>\n' \
                                f"Город: {data['city']}\n" \
                                f"Количество отелей: {data['hotel_amt']}\n" \
                                f"Без фотографий"

            bot.send_message(message.from_user.id, full_info, parse_mode='html')
            bot.send_message(message.from_user.id, choice(['Ожидайте...',
                                                           'Можно 💤? Ждём...',
                                                           'Тик-так ⌛ Ожидаем...',
                                                           'Надеюсь моя 🔋 не сядет...\n'
                                                           'Шучу😉 Просто чуток подождем...',
                                                           'Возьмите пока что 🎧\n'
                                                           'И немного подождем...']))

            low_to_high = "PRICE_LOW_TO_HIGH"
            high_to_low = "PRICE_HIGH_TO_LOW"

            if base_commands.is_low_price:
                sorting = low_to_high
            else:
                sorting = high_to_low

            offers = post_hotels_request(data['cityID'], data['hotel_amt'], sorting)

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
                                     reply_markup=row_address_and_on_map(i_info[0]),
                                     parse_mode='html')
                    count += 1
                else:
                    bot.delete_state(message.from_user.id, message.chat.id)

            elif offers and data['need_photo']:
                sort_offers = sorted(offers.items(), key=lambda val: int(val[1][1][1:]))
                bot.send_message(message.from_user.id, choice(['Подобраны следующие варианты:',
                                                               'Что удалось подобрать:',
                                                               'Подобрал следующее:']))
                count = 1

                for i_offer in sort_offers:
                    offer_with_photo = post_detail_request(i_offer[0], data['photo_amt'])

                    bot.send_message(message.from_user.id,
                                     f'{count}. <b>{i_offer[1][0]}</b>\n'
                                     f'<i>Цена: {i_offer[1][1]}</i>',
                                     reply_markup=row_address_and_on_map(i_offer[0]),
                                     parse_mode='html')
                    count += 1

                    for i_name, i_lst in offer_with_photo.items():
                        if i_name not in ('address', 'static_img'):
                            for i_dct in i_lst:
                                for i_url, i_desc in i_dct.items():
                                    photo_file = requests.get(i_url)
                                    bot.send_photo(message.from_user.id,
                                                   photo_file.url,
                                                   caption=f'{i_desc}')
                else:
                    bot.delete_state(message.from_user.id, message.chat.id)
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
