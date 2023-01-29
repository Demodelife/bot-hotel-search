from loader import bot
from telebot.types import Message
from states.hotel_information import BestDealState
from random import choice


tmp_min_price = 0


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
