from pyrogram.types import Message
from pyrogram.filters import chat
from pyrogram.enums.parse_mode import ParseMode

import re

import db
from init import bot, log_error
from data.chats import chats_flea_market_tbilisi, water_supply, gldanis_lair, gldanis_ads
from utils.message_utils import remove_punctuation
from utils.filters import command_filter
from enums import Commands


recent_text: list = []


# @bot.on_message()
# async def new_chats(client, msg: Message):
    # print(msg.chat.title, msg.chat.id)

@bot.on_message(lambda _, msg: command_filter(msg))
async def new_chats(_, msg: Message):
    try:
        top_text = ''
        if msg.text.startswith(Commands.ADD.value):
            top_text = '<b>Добавлены ключевые слова:</b>\n'
            new_targets = msg.text[4:].split(',')
            title = msg.chat.title if msg.chat.title else 'лс'
            for target in new_targets:
                target_word = target.strip()
                await db.add_order(chat_id=msg.chat.id, target=target_word, title=title)
                top_text = f'{top_text}{target_word}\n'

        elif msg.text.startswith(Commands.DEL.value):
            top_text = '<b>Удалены ключевые слова:</b>\n'
            new_targets = msg.text [4:].split (',')
            for target in new_targets:
                target_word = target.strip()
                await db.del_order (chat_id=msg.chat.id, target=target_word)
                top_text = f'{top_text}{target_word}\n'

        chat_targets = await db.get_orders(chat_id=msg.chat.id)

        if chat_targets:
            target_text = '<b>Целевые слова для чата</b>\n'
            for target in chat_targets:
                target_text = f'{target_text}<code>{target.target}</code>\n'
        else:
            target_text = ''

        text = (f'{top_text}\n'
                f'Я помогу тебе найти товар на барахолках Тбилиси.\n'
                f'Чтобы добавить слова для поиска отправь команду <code>add</code> и список слов или фраз для поиска.\n'
                f'Прекрати поиск отправив <code>del</code> и список слов для удаления\n'
                f'<code>add</code> - добавить целевое слово\n'
                f'<code>del</code> - удалить целевое слово\n'
                f'<code>menu</code> или <code>help</code> - вызов меню\n\n'
                f'{target_text}').strip()

        await bot.send_message(chat_id=msg.chat.id, text=text, parse_mode=ParseMode.HTML)

    except Exception as ex:
        log_error(ex)
        text = 'Ой, ребят, что-то сломалось(( Попробуйте ещё раз, если не пойдёт - сообщите разработчикам'
        await bot.send_message (chat_id=msg.chat.id, text=text, parse_mode=ParseMode.HTML)


@bot.on_message(chat(list(chats_flea_market_tbilisi.values())))
async def flea_market(_, msg: Message):
    global recent_text
    text = msg.text if msg.text else msg.caption

    if text and text not in recent_text:
        orders = await db.get_orders()
        targets = set(word.target for word in orders)

        ignor_chats = []
        for target_word in targets:
            match = re.search(target_word, text, re.IGNORECASE)
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
