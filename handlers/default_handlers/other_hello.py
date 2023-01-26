
from loader import bot
from telebot.types import Message
from random import choice


@bot.message_handler(regexp=r'Привет|Хай|Hello')
def other_hello(message: Message) -> None:
    bot.send_message(message.from_user.id, choice(['Привет, чем я могу вам помочь?\n'
                                                   'Для списка моих команд /help',
                                                   'Привет, если понадобятся мои команды,\n'
                                                   'То вам сюда /help',
                                                   'Привет!\n'
                                                   'Для справки переходите сюда /help',
                                                   'Приветствую!\n'
                                                   'Список моих команд тут /help',
                                                   'Привет, я помогу вам!\n'
                                                   'Только выберите одну из моих команд тут /help']))
