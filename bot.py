from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from utils import temp

class Bot(Client):

    def __init__(self):
        super().__init__(
            "anime bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins"),
            workers=150,
            sleep_threshold=5
        )

      
    async def start(self):
            
        await super().start()
        me = await self.get_me()
        self.username = '@' + me.username
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        print('Bot Started.')


    async def stop(self, *args):

        await super().stop()
        print('Bot Stopped Bye')

Bot().run()
