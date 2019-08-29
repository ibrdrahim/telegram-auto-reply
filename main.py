#!/usr/bin/env python3
# A simple script to print some messages.
import os
import sys
import time
import re

from telethon import TelegramClient, events, utils

def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)


session = os.environ.get('TG_SESSION', 'printer')
api_id = 'YOUR API ID'
api_hash = 'YOUR API HASH'
telegram_username = 'YOUR TELEGRAM USERNAME'
proxy = None  # https://github.com/Anorov/PySocks

# Create and start the client so we can make requests (we don't here)
client = TelegramClient(session, api_id, api_hash, proxy=proxy).start()

@client.on(events.NewMessage)
async def handle_new_message(event):
    if event.is_private or re.search(telegram_username,event.raw_text):  # only auto-reply to private chats
        from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
        if not from_.bot:  # don't auto-reply to bots
            print(time.asctime(), '-', event.message)  # optionally log time and message
            time.sleep(1)  # pause for 1 second to rate-limit automatic replies
            await event.reply(
                "**AUTO REPLY**" 
                "\n\nMaaf boss saya sedang offline, mohon tunggu sebentar."
                "\nSilahkan lihat-lihat [imacakes](https://www.instagram.com/ima_cake_cirebon) dulu untuk cuci mata."
                "\n\n**AUTO REPLY**" 
                ) # setup your reply message here

client.start()
client.run_until_disconnected()