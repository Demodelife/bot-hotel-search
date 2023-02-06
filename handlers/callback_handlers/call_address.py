from loader import bot
from telebot.types import CallbackQuery
from utils.api_requests.detail_request import post_detail_request
from loguru import logger


@logger.catch
@bot.callback_query_handler(func=lambda call: call.data.startswith('add'))
def callback_address(callback_query: CallbackQuery) -> None:
    """Колбэк-хэндлер, обрабатывающий inline-кнопку 'Адрес отеля' """

    response = post_detail_request(callback_query.data[3:])
    result = '\n'.join(['<b>Отель:</b>',
                        f"<i>{response['name']}</i>",
                        '<b>Адрес:</b>',
                        f"<i>{response['address']}</i>"])
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, result, parse_mode='html')
