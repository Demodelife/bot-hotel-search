from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def row_address_and_on_map(hotel_id) -> InlineKeyboardMarkup:
    row_kb = InlineKeyboardMarkup()
    address_kb = InlineKeyboardButton('Адрес отеля', callback_data='add' + hotel_id)
    on_map_kb = InlineKeyboardButton('На карте', callback_data='map' + hotel_id)
    row_kb.row(address_kb, on_map_kb)
    return row_kb

# print(row_address_and_on_map('31702975'))
