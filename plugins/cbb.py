from pyrogram import __version__
from bot import Bot
from config import OWNER_ID

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        # Your existing implementation
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('enable_auto_delete'))
async def enable_auto_delete(client: Bot, message: Message):
    # Ensure AUTO_DELETE_ENABLED is set to True
    client.config.AUTO_DELETE_ENABLED = True
    await message.reply("Auto-deletion feature enabled.")

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('disable_auto_delete'))
async def disable_auto_delete(client: Bot, message: Message):
    # Ensure AUTO_DELETE_ENABLED is set to False
    client.config.AUTO_DELETE_ENABLED = False
    await message.reply("Auto-deletion feature disabled.")
