from loader import bot
from telebot.types import CallbackQuery
from loguru import logger
from utils.create_search_history_db import *
from keyboards.inline.all_keyboards import delete_history


@logger.catch
@bot.callback_query_handler(func=lambda call: call.data.startswith('last'))
def callback_history(callback_query: CallbackQuery) -> None:

    limit_cnt = 0

    if User.get_or_none(userID=callback_query.from_user.id):

        if callback_query.data.endswith('five'):
            limit = 5

        else:
            limit = 1

        for i_user in reversed(User.select()):

            if limit_cnt == limit:
                break

            if callback_query.from_user.id == i_user.userID:

                info_user = '\n'.join(['Пользователь: ' + i_user.name,
                                       'Команда: /' + i_user.command,
                                       'Время запроса: ' + f'<i>{i_user.time}</i>'])
                bot.send_message(callback_query.from_user.id, info_user, parse_mode='html')

                if i_user.command == 'lowprice':

                    for i_hotel in i_user.hotels_lp:
                        if i_hotel.owner_id == i_user.id:
                            info_hotel = '\n'.join(['Город: ' + i_hotel.city,
                                                    'Отель: ' + f'<b>{i_hotel.name}</b>',
                                                    'Цена: ' + f'<i>{i_hotel.price}</i>'])
                            bot.send_message(callback_query.from_user.id, info_hotel, parse_mode='html')

                    else:
                        bot.send_message(callback_query.from_user.id, '_' * 35)
                        limit_cnt += 1

                elif i_user.command == 'highprice':
                    for i_hotel in i_user.hotels_hp:
                        if i_hotel.owner_id == i_user.id:
                            info_hotel = '\n'.join(['Город: ' + i_hotel.city,
                                                    'Отель: ' + f'<b>{i_hotel.name}</b>',
                                                    'Цена: ' + f'<i>{i_hotel.price}</i>'])
                            bot.send_message(callback_query.from_user.id, info_hotel, parse_mode='html')

                    else:
                        bot.send_message(callback_query.from_user.id, '_' * 35)
                        limit_cnt += 1

                else:
                    for i_hotel in i_user.hotels_bd:
                        if i_hotel.owner_id == i_user.id:
                            info_hotel = '\n'.join(['Город: ' + i_hotel.city,
                                                    'Отель: ' + f'<b>{i_hotel.name}</b>',
                                                    'Цена: ' + f'<i>{i_hotel.price}</i>',
                                                    'Расстояние до центра: ' + f'<i>{i_hotel.distance} км</i>'])
                            bot.send_message(callback_query.from_user.id, info_hotel, parse_mode='html')

                    else:
                        bot.send_message(callback_query.from_user.id, '_' * 35)
                        limit_cnt += 1

        bot.send_message(callback_query.from_user.id, 'Очистить историю ваших запросов? 🚮',
                         reply_markup=delete_history())

    else:
        bot.send_message(callback_query.from_user.id, 'Ваша история пуста 🤷')


@logger.catch
@bot.callback_query_handler(func=lambda call: call.data == 'delete')
def callback_delete_history(callback_query: CallbackQuery) -> None:

    for i_user in User.select():
        if callback_query.from_user.id == i_user.userID:

            for i_hotel in i_user.hotels_lp:
                if i_hotel.owner_id == i_user.id:
                    i_hotel.delete_instance()

            for i_hotel in i_user.hotels_hp:
                if i_hotel.owner_id == i_user.id:
                    i_hotel.delete_instance()

            for i_hotel in i_user.hotels_bd:
                if i_hotel.owner_id == i_user.id:
                    i_hotel.delete_instance()

            i_user.delete_instance()
    else:
        bot.send_message(callback_query.from_user.id, 'История запросов полностью очищена! ✅')