from telebot.types import Message
from loader import bot


@bot.message_handler(state=None)
def bot_echo(message: Message):
    """Эхо-бот без состояния, отвечающий повторением сообщения от пользователя"""

    bot.reply_to(message, f"Для выбора команды для меня переходите сюда - /help\n"
                          f"Иначе я простая повторюшка🙃: {message.text}")
