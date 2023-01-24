
from loader import bot
from telebot.types import Message


@bot.message_handler()
def other_hello(message: Message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, 'Привет, чем я могу тебе помочь?')
    else:
        bot.send_message(message.from_user.id, 'Пока что я тебя не понимаю...')