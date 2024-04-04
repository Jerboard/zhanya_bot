from pyrogram.types import Message
from pyrogram.filters import chat

from init import bot, last_ads
from data.chats import chats_flea_market_tbilisi, water_supply, gldanis_lair, gldanis_ads
from utils.message_utils import remove_punctuation


recent_text: list = []

# @bot.on_message()
# async def new_chats(client, msg: Message):
#     print(msg.chat.title, msg.chat.id)


@bot.on_message(chat(list(chats_flea_market_tbilisi.values())))
async def flea_market(client, msg: Message):
    global recent_text
    text = msg.text if msg.text else msg.caption

    if text not in recent_text:
        clear_text = remove_punctuation(text)

        target = ['стол', 'стул', 'стулья', 'утюг']

        for word in clear_text:
            if word in target:

                await bot.forward_messages(
                    chat_id=gldanis_ads,
                    from_chat_id=msg.chat.id,
                    message_ids=msg.id
                )
                recent_text.append (text)
                if len (recent_text) >= 10:
                    recent_text = recent_text [-10:]

                try:
                    text_link = f'<a href="https://t.me/{msg.chat.username}/{msg.id}"><b>Оригинал</b></a>'
                    await bot.send_message(chat_id=gldanis_ads, text=text_link, parse_mode='html')

                except Exception as ex:
                    text_link = f'@{msg.chat.username}\n\n{ex}'
                    await bot.send_message (chat_id=gldanis_ads, text=text_link, parse_mode='html')
                finally:
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
