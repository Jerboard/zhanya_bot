from handlers import bot
from config import config

import logging
import sys


if __name__ == '__main__':
    if config.debug:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    else:
        logging.basicConfig (level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s", filename='log.log')
    bot.run()
