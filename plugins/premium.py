from datetime import timedelta
from asyncio import sleep 
import pytz
import datetime, time
from config import ADMINS, LOG_CHANNEL
from plugins.database import db 
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
import traceback

async def get_seconds(time_string):
    def extract_value_and_unit(ts):
        value = ""
        unit = ""
        index = 0
        while index < len(ts) and ts[index].isdigit():
            value += ts[index]
            index += 1
        unit = ts[index:].lstrip()
        if value:
            value = int(value)
        return value, unit
    value, unit = extract_value_and_unit(time_string)
    if unit == 's':
        return value
    elif unit == 'min':
        return value * 60
    elif unit == 'hour':
        return value * 3600
    elif unit == 'day':
        return value * 86400
    elif unit == 'month':
        return value * 86400 * 30
    elif unit == 'year':
        return value * 86400 * 365
    else:
        return 0

@Client.on_message(filters.command("premium") & filters.user(ADMINS))
async def add_premium(client, message):
    try:
        _, user_id, time, *custom_message = message.text.split(" ", 3)
        custom_message = "**Tʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴘᴜʀᴄʜᴀsɪɴɢ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ ᴘᴀᴄᴋᴀɢᴇ. Nᴏᴡ, ʟᴇᴠᴇʀᴀɢᴇ ɪᴛs ғᴜʟʟ ᴘᴏᴛᴇɴᴛɪᴀʟ**" if not custom_message else " ".join(custom_message)
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y : %I:%M:%S %p")
        user = await client.get_users(user_id)
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + timedelta(seconds=seconds)
            user_data = {"id": user.id, "expiry_time": expiry_time}
            await db.update_user(user_data)
            await db.set_plan(user.id, plan=True)
            data = await db.get_user(user.id)
            expiry = data.get("expiry_time")
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y  :  %I:%M:%S %p")
            await message.reply_text(f"<b><u>Premium Access Added To The User</u>\n\n👤 User: {user.mention}\n\n🪪 User id: <code>{user_id}</code>\n\n⏰ Premium Access: {time}\n\n🎩 Joining : {current_time}\n\n⌛️ Expiry: {expiry_str_in_ist}.\n\n<code>{custom_message}</code></b>", disable_web_page_preview=True)
            await client.send_message(chat_id=user_id, text=f"<b>ʜɪɪ {user.mention},\n\n<u>ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ</u> 😀\n\nᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss - {time}\n\n⏰ ᴊᴏɪɴɪɴɢ - {current_time}\n\n⌛️ ᴇxᴘɪʀᴇ ɪɴ - {expiry_str_in_ist}\n\n<code>{custom_message}</code></b>", disable_web_page_preview=True)
            await client.send_message(LOG_CHANNEL, text=f"#Added_Premium\n\n👤 User - {user.mention}\n\n🪪 User Id - <code>{user_id}</code>\n\n⏰ Premium Access - {time}\n\n🎩 Joining - {current_time}\n\n⌛️ Expiry - {expiry_str_in_ist}\n\n<code>{custom_message}</code>", disable_web_page_preview=True)
        else:
            await message.reply_text("<b>⚠️ Invalid Format, Use This Format - <code>/premium 1030335104 1day</code>\n\n<u>Time Format -</u>\n\n<code>1 day for day\n1 hour for hour\n1 min for minutes\n1 month for month\n1 year for year</code>\n\nChange As Your Wish Like 2, 3, 4, 5 etc....</b>")
    except ValueError:
        await message.reply_text("<b>⚠️ Invalid Format, Use This Format - <code>/premium 1030335104 1day</code>\n\n<u>Time Format -</u>\n\n<code>1 day for day\n1 hour for hour\n1 min for minutes\n1 month for month\n1 year for year</code>\n\nChange As Your Wish Like 2, 3, 4, 5 etc....</b>")
    except Exception as e:
        traceback.print_exc()
        await message.reply_text(f"error - {e}")


@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("<b>sᴜᴄᴄᴇssꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ 💔</b>")
            await db.set_plan(user_id, plan=False)
            await client.send_message(
                chat_id=user_id,
                text=f"<b>ʜᴇʏ {user.mention},\n\nʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ 😕</b>"
            )
        else:
            await message.reply_text("<b>👀 ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ, ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ɪᴛ ᴡᴀs ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜsᴇʀ ɪᴅ??</b>")
    else:
        await message.reply_text("Usage: <code>/remove_premium user_id</code>")

    
