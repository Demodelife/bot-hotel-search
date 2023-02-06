from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    """Базовый хэндлер команды /start, предлагает воспользоваться /help"""

    bot.reply_to(message, f"Привет, {message.from_user.full_name}!\n"
                          f"Всё, что я умею тут - /help")
