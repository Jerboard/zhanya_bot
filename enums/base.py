from enum import Enum


class Commands(str, Enum):
    ADD = 'add '
    DEL = 'del '
    HELP = 'help'
    MENU = 'menu'
