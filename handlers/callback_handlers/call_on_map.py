from loader import bot
from telebot.types import CallbackQuery
from utils.api_requests.detail_request import post_detail_request
import requests
from loguru import logger


@logger.catch
@bot.callback_query_handler(func=lambda call: call.data.startswith('map'))
def callback_on_map(callback_query: CallbackQuery) -> None:
    """Колбэк-хэндлер, обрабатывающий inline-кнопку 'На карте' """

    response = post_detail_request(callback_query.data[3:])
    image_url = response['static_img']
    photo_file = requests.get(image_url)

    result = '\n'.join(['<b>Отель:</b>',
                        f"<i>{response['name']}</i>",
                        '<b>Адрес:</b>',
                        f"<i>{response['address']}</i>"])
    bot.answer_callback_query(callback_query.id)
    bot.send_photo(callback_query.from_user.id,
                   photo_file.url,
                   caption=result,
                   parse_mode='html')
