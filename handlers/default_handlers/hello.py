from loader import bot
from telebot.types import Message
from random import choice


@bot.message_handler(commands=['hello'])
def bot_hello(message: Message) -> None:
    """Хэндлер команды /hello, приветствует пользователя"""

    bot.send_message(message.from_user.id, choice([f'Приветствую вас снова, {message.from_user.full_name}!',
                                                   f'И снова здравствуйте, {message.from_user.full_name}!',
                                                   f'Добро пожаловать, {message.from_user.full_name}!',
                                                   f'Рад вас видеть, {message.from_user.full_name}!',
                                                   f'Я рад, что вы ко мне заглянули, {message.from_user.full_name}!']))
