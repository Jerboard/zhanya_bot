from pyrogram import Client
from sqlalchemy.ext.asyncio import create_async_engine

import asyncio
import logging
import traceback
import os
from datetime import datetime

from config import config

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

try:
    bot = Client("zhenya")
except:
    bot = Client("zhenya", api_id=config.API_ID, api_hash=config.API_HAS)

ENGINE = create_async_engine (url=config.db_url)


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
        logging.warning(f'{now}\n{ex_traceback}\n{message}')
    else:
        logging.warning(f'{now}\n{message}')
