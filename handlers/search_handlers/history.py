from loader import bot
from telebot.types import Message
from keyboards.inline.all_keyboards import row_show_history


@bot.message_handler(commands=['history'])
def show_history(message: Message) -> None:
    """Хэндлер команды /history, предлагает ряд inline-кнопок для выбора нужного колбэка"""

    bot.send_message(message.from_user.id, 'Выберите количество запросов:',
                     reply_markup=row_show_history())
