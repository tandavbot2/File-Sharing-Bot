from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    # Your existing implementation

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    # Your existing implementation

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('enable_auto_delete'))
async def enable_auto_delete(client: Client, message: Message):
    # Ensure AUTO_DELETE_ENABLED is set to True
    client.config.AUTO_DELETE_ENABLED = True
    await message.reply("Auto-deletion feature enabled.")

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('disable_auto_delete'))
async def disable_auto_delete(client: Client, message: Message):
    # Ensure AUTO_DELETE_ENABLED is set to False
    client.config.AUTO_DELETE_ENABLED = False
    await message.reply("Auto-deletion feature disabled.")
