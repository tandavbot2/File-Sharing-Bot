import asyncio
from datetime import datetime, timedelta
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, AUTO_DELETE_TIME, AUTO_DELETE_ENABLED
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'users', 'broadcast', 'batch', 'genlink', 'stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return

    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)

    if AUTO_DELETE_ENABLED:
        # Notify user about auto-deletion
        notification_msg = await message.reply_text(
            f"Please forward the files you received. These files will be deleted in {AUTO_DELETE_TIME / 60} minutes.",
            quote=True
        )
        # Schedule file deletion
        await asyncio.sleep(AUTO_DELETE_TIME)
        try:
            # Delete the notification message
            await notification_msg.delete()
            # Delete all forwarded messages from the user
            async for msg in client.get_chat_history(message.chat.id):
                if msg.date > (datetime.now() - timedelta(seconds=AUTO_DELETE_TIME)):
                    await msg.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")
