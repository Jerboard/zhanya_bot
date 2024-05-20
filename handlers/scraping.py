from pyrogram.types import Message
from pyrogram.filters import chat
from pyrogram.enums.parse_mode import ParseMode

import re

import db
from init import bot, log_error
from data.chats import chats_flea_market_tbilisi, water_supply, gldanis_lair, gldanis_ads
from utils.message_utils import remove_punctuation


recent_text: list = []


@bot.on_message(chat(list(chats_flea_market_tbilisi.values())))
async def flea_market(_, msg: Message):
    global recent_text
    text = msg.text if msg.text else msg.caption

    if text and text not in recent_text:
        orders = await db.get_orders()
        targets = set(word.target for word in orders)

        ignor_chats = []
        for target_word in targets:
            match = re.search(target_word.replace('*', '\W'), text, re.IGNORECASE)
            if match:
                recent_text.append (text)
                if len (recent_text) >= 10:
                    recent_text = recent_text [-10:]

                text_link = f'<a href="https://t.me/{msg.chat.username}/{msg.id}"><b>Оригинал</b></a>'

                for order in orders:
                    if order.target == target_word and order.chat_id not in ignor_chats:
                        await bot.forward_messages (
                            chat_id=order.chat_id,
                            from_chat_id=msg.chat.id,
                            message_ids=msg.id
                        )
                        await bot.send_message(chat_id=order.chat_id, text=text_link, disable_web_page_preview=True)
                        ignor_chats.append(order.chat_id)


@bot.on_message(chat(water_supply))
async def water_supply(client, msg: Message):
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
