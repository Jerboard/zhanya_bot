from dotenv import load_dotenv
from os import getenv

from pytz import timezone


load_dotenv ()


class config:
    debug = bool(int(getenv('DEBUG')))
    tz = timezone('Asia/Tbilisi')
    FILTER_CHAT_DATA_NAME = getenv('FILTER_CHAT_DATA_NAME')
    START_LINK = getenv ('START_LINK')

    DATETIME_STR_FORMAT = '%d.%m.%y %H:%M'

    SEND_ERROR_ID = getenv('SEND_ERROR_ID')
    INVOICE_LINK_NAME = getenv('INVOICE_LINK_NAME')
    UB_USERNAME = getenv('UB_USERNAME')

    API_ID = getenv('API_ID')
    API_HAS = getenv('API_HAS')

    db_url = getenv ('DB_URL')