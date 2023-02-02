from os import path
from loguru import logger


def start_logger() -> None:
    """Функция, запускающая log файл"""

    logger.add(path.join('database', 'errors.log'),
               format='{time:DD-MMM-YYYY at HH:mm:ss-Z} {level} {message}',
               level='ERROR',
               rotation='100 KB',
               compression='zip')
