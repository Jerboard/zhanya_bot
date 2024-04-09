from pyrogram.types import Message

from enums import Commands


def command_filter(msg: Message):
    result = False
    try:
        if msg.text and msg.text[:4].lower() in [Commands.ADD.value,
                                                 Commands.DEL.value,
                                                 Commands.MENU.value,
                                                 Commands.HELP.value]:
            result = True
    except Exception as ex:
        print(ex)

    return result
