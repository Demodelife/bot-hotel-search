from loader import bot
from telebot.custom_filters import StateFilter
import handlers
from utils.set_bot_commands import set_default_commands
from utils.logger_script import start_logger
from database.hotels_db import db, tables


def main() -> None:

    if not all(i_tab.table_exists() for i_tab in tables):
        db.create_tables(tables)

    if __name__ == '__main__':
        start_logger()
        bot.add_custom_filter(StateFilter(bot))
        set_default_commands(bot)
        bot.infinity_polling()


main()
