from pyrogram import __version__
from bot import Bot
from config import ADMINS, OWNER_ID, AUTO_DELETE_ENABLED
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import filters
from pyrogram.types import Message

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text=f"<b>○ Creator : <a href='tg://user?id={OWNER_ID}'>This Person</a>\n○ Language : <code>Python3</code>\n○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a>\n○ Source Code : <a href='PRIVATE'>Click here</a>\n○ Channel : @TandavBots\n○ Support Group : @@TandavBot_Support</b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data="close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

@Bot.on_message(filters.private & filters.text)
async def handle_auto_delete(client: Bot, message: Message):
    if AUTO_DELETE_ENABLED:
        # Send notification message with file deletion info
        await message.reply_text(
            "Your files will be automatically deleted in 10 minutes. Please make sure to download or forward them before the deletion occurs.",
            quote=True
        )
        
        # Schedule file deletion after 10 minutes (600 seconds)
        await asyncio.sleep(600)
        
        # Attempt to delete the user's message
        try:
            await message.delete()
        except:
            pass
