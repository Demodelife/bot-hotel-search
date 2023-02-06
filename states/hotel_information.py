from telebot.handler_backends import State, StatesGroup


class HotelInfoState(StatesGroup):
    """Класс состояний для команд: /lowprice, /highprice"""

    city = State()
    hotel_amt = State()
    need_photo = State()
    photo_amt = State()
    info_low_high = State()


class BestDealState(HotelInfoState):
    """Класс состояний для команды /bestdeal"""

    price_min = State()
    price_max = State()
    distance = State()
    info_best_deal = State()
