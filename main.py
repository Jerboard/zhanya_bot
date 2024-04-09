from handlers import bot
from config import config
from init import log_error

import logging
import sys


if __name__ == '__main__':
    if config.debug:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        log_error(message='start_bot', with_traceback=False)
    bot.run ()
