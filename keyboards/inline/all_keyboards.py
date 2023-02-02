from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def row_address_and_on_map(hotel_id: str) -> InlineKeyboardMarkup:
    row_kb = InlineKeyboardMarkup()
    address_kb = InlineKeyboardButton('Адрес отеля', callback_data='add' + hotel_id)
    on_map_kb = InlineKeyboardButton('На карте', callback_data='map' + hotel_id)
    row_kb.row(address_kb, on_map_kb)
    return row_kb


def row_show_history() -> InlineKeyboardMarkup:
    row_kb = InlineKeyboardMarkup()
    show_last = InlineKeyboardButton('Последний запрос', callback_data='last')
    show_last_five = InlineKeyboardButton('Последние 5 запросов', callback_data='last_five')
    row_kb.row(show_last, show_last_five)
    return row_kb


def delete_history() -> InlineKeyboardMarkup:
    key = InlineKeyboardMarkup()
    key.add(InlineKeyboardButton('Да, очистить', callback_data='delete'))
    return key

