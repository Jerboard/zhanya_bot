from pyrogram import Client
from sqlalchemy.ext.asyncio import create_async_engine

import asyncio
import logging
import traceback
import os
import re
from datetime import datetime

from config import config

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

bot = Client("zhenya", api_id=config.API_ID, api_hash=config.API_HAS)

ENGINE = create_async_engine (url=config.db_url)


# запись ошибок
def log_error(message, with_traceback: bool = True):
    now = datetime.now(config.tz)
    log_folder = now.strftime ('%m-%Y')
    log_path = os.path.join('logs', log_folder)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_file_path = os.path.join(log_path, f'{now.day}.log')
    logging.basicConfig (level=logging.WARNING, filename=log_file_path, encoding='utf-8')
    if with_traceback:
        ex_traceback = traceback.format_exc()
        tb = ''
        start_row = '  File'  # if config.debug else '  File "/home'
        tb_split = ex_traceback.split('\n')
        for row in tb_split:
            if row.startswith(start_row) and not re.search ('venv', row):
                tb += f'{row}\n'

        msg = ex_traceback.split('\n\n')[-1]
        logging.warning(f'{now}\n{tb}\n{msg}\n---------------------------------\n')
    else:
        logging.warning(f'{now}\n{message}\n\n---------------------------------\n')
