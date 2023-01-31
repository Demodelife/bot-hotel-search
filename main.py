from loader import bot
from telebot.custom_filters import StateFilter
import handlers
from utils.set_bot_commands import set_default_commands
from utils.logger_script import start_logger


if __name__ == '__main__':
    start_logger()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
