from pyrogram.types import Message
from pyrogram.enums.parse_mode import ParseMode

import db
from init import bot, log_error
from utils.filters import command_filter
from enums import Commands


# async def test_send():
#     await bot.start()
#     text = 'test'
#     await bot.send_message (chat_id=-1001669708234, text=text, parse_mode=ParseMode.HTML)


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
            target_text = '<b>Целевые слова для чата:</b>\n'
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
        text = 'Ой, ребят, что-то сломалось(( Попробуйте ещё раз, если не пойдёт - сообщите разработчику'
        await bot.send_message (chat_id=msg.chat.id, text=text, parse_mode=ParseMode.HTML)
