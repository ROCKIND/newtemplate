from pyrogram import Client, filters
from config import FILE_CHANNEL
from plugins.database import save_message

filter = filters.video

@Client.on_message(filters.chat(FILE_CHANNEL) & filter)
async def save(bot, message):
    if message.video:
        file_id = message.video.file_id
        file_size = message.video.duration
        caption = "Sex Porn Xxx"
        
    await save_message(caption, file_id, message.id, file_size)
            
