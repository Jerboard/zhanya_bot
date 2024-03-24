from pyrogram import Client
# from sqlalchemy.ext.asyncio import create_async_engine

import asyncio
import logging
import traceback
from datetime import datetime

from config import config

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

bot = Client("zhenya", api_id=config.API_ID, api_hash=config.API_HAS)


def log_error(message):
    timestamp = datetime.now()
    filename = traceback.format_exc()[1]
    line_number = traceback.format_exc()[2]
    logging.error(f'{timestamp} {filename} {line_number}: {message}')
