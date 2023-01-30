from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(message, f"Для выбора команды для меня переходите сюда - /help\n"
                          f"Иначе я простая повторюшка🙃: {message.text}")
