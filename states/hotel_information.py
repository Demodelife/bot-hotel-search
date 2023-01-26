from telebot.handler_backends import State, StatesGroup


class HotelInfoState(StatesGroup):
    city = State()
    hotel_amt = State()
    need_photo = State()
    photo_amt = State()
    info_low_high = State()


class BestDealState(HotelInfoState):
    price_min = State()
    price_max = State()
    distance = State()
    info_best_deal = State()
