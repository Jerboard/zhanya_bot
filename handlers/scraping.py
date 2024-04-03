from pyrogram.types import Message
from pyrogram.filters import chat

from init import bot
from data.chats import chats_flea_market_tbilisi, water_supply, gldanis_lair
from utils.message_utils import remove_punctuation


# @bot.on_message()
# async def new_chats(client, msg: Message):
#     print(msg.chat.title, msg.chat.id)


@bot.on_message(chat(list(chats_flea_market_tbilisi.values())))
async def flea_market(client, msg: Message):
    text = msg.text if msg.text else msg.caption
    clear_text = remove_punctuation(text)

    target = ['стол', 'стул', 'стулья', 'утюг']

    for word in clear_text:
        if word in target:
            await bot.forward_messages(
                chat_id=gldanis_lair,
                from_chat_id=msg.chat.id,
                message_ids=msg.id
            )
            break


@bot.on_message(chat(water_supply))
async def flea_market(client, msg: Message):
    text = msg.text if msg.text else msg.caption
    clear_text = remove_punctuation(text)

    target = ['khizabavari',]

    for word in clear_text:
        if word in target:
            await bot.forward_messages (
                chat_id=gldanis_lair,
                from_chat_id=msg.chat.id,
                message_ids=msg.id
            )
            break
