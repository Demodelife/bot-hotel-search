
from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['hello'])
def bot_hello(message: Message):
    bot.send_message(message.from_user.id, f'Приветствую тебя снова, {message.from_user.full_name}!')



