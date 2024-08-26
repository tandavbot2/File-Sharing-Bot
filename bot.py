#(©)Codexbotz

from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        try:
            await super().start()
            usr_bot_me = await self.get_me()
            self.uptime = datetime.now()

            if FORCE_SUB_CHANNEL:
                try:
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                    if not link:
                        await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                        link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                    self.invitelink = link
                except Exception as e:
                    self.LOGGER(__name__).warning(f"Failed to get or export invite link for FORCE_SUB_CHANNEL: {e}")
                    self.LOGGER(__name__).warning("Ensure bot is admin and has correct permissions.")
                    sys.exit()

            try:
                db_channel = await self.get_chat(CHANNEL_ID)
                self.db_channel = db_channel
                test = await self.send_message(chat_id=db_channel.id, text="Test Message")
                await test.delete()
            except Exception as e:
                self.LOGGER(__name__).warning(f"Failed to send test message to CHANNEL_ID: {e}")
                self.LOGGER(__name__).warning("Ensure bot is admin in DB Channel and CHANNEL_ID is correct.")
                sys.exit()

            self.set_parse_mode(ParseMode.HTML)
            self.LOGGER(__name__).info(f"Bot Running!\n\nCreated by \nhttps://t.me/CodeXBotz")
            self.LOGGER(__name__).info("""
░█████╗░░█████╗░██████╗░███████╗██╗░░██╗██████╗░░█████╗░████████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗╚══██╔══╝╚════██║
██║░░╚═╝██║░░██║██║░░██║█████╗░░░╚███╔╝░██████╦╝██║░░██║░░░██║░░░░░███╔═╝
██║░░██╗██║░░██║██║░░██║██╔══╝░░░██╔██╗░██╔══██╗██║░░██║░░░██║░░░██╔══╝░░
╚█████╔╝╚█████╔╝██████╔╝███████╗██╔╝╚██╗██████╦╝╚█████╔╝░░░██║░░░███████╗
░╚════╝░░╚════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚══════╝
            """)
            self.username = usr_bot_me.username

            # Web server setup
            app = web.AppRunner(await web_server())
            await app.setup()
            bind_address = "0.0.0.0"
            await web.TCPSite(app, bind_address, PORT).start()

        except Exception as e:
            self.LOGGER(__name__).error(f"Error during bot startup: {e}")
            sys.exit()

    async def stop(self, *args):
        try:
            await super().stop()
            self.LOGGER(__name__).info("Bot stopped.")
        except Exception as e:
            self.LOGGER(__name__).error(f"Error stopping the bot: {e}")

# Ensure the bot is started only if this script is run directly
if __name__ == "__main__":
    bot = Bot()
    bot.run()
