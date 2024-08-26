# cbb.py
from pyrogram import __version__
from bot import Bot
from config import OWNER_ID, ADMINS
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait
from pyrogram import filters


AUTO_DELETE_ENABLED = True  # Default state

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('enable_auto_delete'))
async def enable_auto_delete(client: Bot, message: Message):
    global AUTO_DELETE_ENABLED
    AUTO_DELETE_ENABLED = True
    await message.reply("Auto-deletion has been <b>enabled</b>.", parse_mode='html')

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('disable_auto_delete'))
async def disable_auto_delete(client: Bot, message: Message):
    global AUTO_DELETE_ENABLED
    AUTO_DELETE_ENABLED = False
    await message.reply("Auto-deletion has been <b>disabled</b>.", parse_mode='html')

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = f"<b>○ Creator : <a href='tg://user?id={OWNER_ID}'>This Person</a>\n○ Language : <code>Python3</code>\n○ Library : <a href='https://docs.pyrogram.org/'>Pyrogram asyncio {__version__}</a>\n○ Source Code : <a href='PRIVATE'>Click here</a>\n○ Channel : @TandavBots\n○ Support Group : @@TandavBot_Support</b>",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
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
