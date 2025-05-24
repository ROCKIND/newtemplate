import asyncio, re, os, json
import random
from pyrogram import Client, filters, enums
from config import LOG_CHANNEL, FILE_CHANNEL, AUTH_CHANNEL, SECOND_AUTH_CHANNEL, FORWARD, REQUEST_TO_JOIN_MODE
from plugins.database import db, save_message, get_search_results
from plugins.join_reqs import JoinReqs
from pyrogram.errors import *
from utils import temp 
from datetime import datetime
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
    ChatJoinRequest,
    KeyboardButton,
    ReplyKeyboardMarkup
)

LOG_TEXT = """<b>#NewUser\n\nID - <code>{}</code>\n\nNᴀᴍᴇ - {}</b>"""
join_db = JoinReqs

BRA_TXT = """𝖡𝗎𝗒 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 𝖠𝗇𝖽 𝖦𝖾𝗍 900+ 𝖡𝖺𝗋𝗓𝗓𝖾𝗋𝗌 𝖵𝗂𝖽𝖾𝗈 𝖯𝖾𝗋 𝖬𝗈𝗇𝗍𝗁."""

SUBS_TXT = """𝖯𝗎𝗋𝖼𝗁𝖺𝗌𝖾 𝖮𝗎𝗋 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 𝖳𝗈 𝖡𝗈𝗈𝗌𝗍 𝖸𝗈𝗎 𝖣𝖺𝗂𝗅𝗒 𝖫𝗂𝗆𝗂𝗍𝗌.

<blockquote>𝖥𝗋𝖾𝖾 𝖴𝗌𝖾𝗋 𝖡𝖾𝗇𝖾𝖿𝗂𝗍𝗌</blockquote>
» 𝖦𝖾𝗍 𝖣𝖺𝗂𝗅𝗒 5 𝖥𝗂𝗅𝖾𝗌 𝖣𝖺𝗂𝗅𝗒
» 𝖬𝖺𝗑𝗂𝗆𝗎𝗆 𝖵𝗂𝖽𝖾𝗈 𝖫𝖾𝗇𝗀𝗍𝗁 5 𝖬𝗂𝗇𝗎𝗍𝖾𝗌 
» 𝖭𝗈 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖢𝗈𝗇𝗍𝖾𝗇𝗍

<blockquote>𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖴𝗌𝖾𝗋 𝖡𝖾𝗇𝖾𝖿𝗂𝗍𝗌</blockquote>
» 𝖦𝖾𝗍 𝖣𝖺𝗂𝗅𝗒 40 𝖥𝗂𝗅𝖾𝗌 𝖣𝖺𝗂𝗅𝗒 
» 𝖬𝖺𝗑𝗂𝗆𝗎𝗆 𝖵𝗂𝖽𝖾𝗈 𝖫𝖾𝗇𝗀𝗍𝗁 𝖴𝗇𝗅𝗂𝗆𝗂𝗍𝖾𝖽
» 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖢𝗈𝗇𝗍𝖾𝗇𝗍    
  
<blockquote>𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 𝖯𝗋𝗂𝖼𝖾</blockquote> 
1 𝖬𝗈𝗇𝗍𝗁 - 50𝖱𝗌 
2 𝖬𝗈𝗇𝗍𝗁 - 90𝖱𝗌  
3 𝖬𝗈𝗇𝗍𝗁 - 130𝖱𝗌 
4 𝖬𝗈𝗇𝗍𝗁 - 150𝖱𝗌 

𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖮𝗐𝗇𝖾𝗋 𝖥𝗈𝗋 𝖬𝗈𝗋𝖾 𝖨𝗇𝖿𝗈𝗋𝗆𝖺𝗍𝗂𝗈𝗇 𝖠𝖻𝗈𝗎𝗍 𝖯𝖺𝗒𝗆𝖾𝗇𝗍."""

PLAN_TXT = """<blockquote>𝖯𝗅𝖺𝗇 𝖣𝖾𝗍𝖺𝗂𝗅𝗌</blockquote>

𝖴𝗌𝖾𝗋 𝖭𝖺𝗆𝖾 - {}
𝖴𝗌𝖾𝗋 𝖨𝖣 - {}
𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 - {}
𝖣𝖺𝗂𝗅𝗒 𝖥𝗂𝗅𝖾𝗌 𝖫𝗂𝗆𝗂𝗍𝗌 - {} 𝖥𝗂𝗅𝖾𝗌
𝖥𝗂𝗅𝖾𝗌 𝖴𝗌𝖾𝖽 - {}/{}
𝖥𝗂𝗅𝖾𝗌 𝖱𝖾𝗆𝖺𝗂𝗇𝗂𝗇𝗀 - {} 𝖥𝗂𝗅𝖾𝗌"""

keyboard = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("Get Video"),
            KeyboardButton("Brazzers")
        ],
        [
            KeyboardButton("My Plan"),
            KeyboardButton("Subscription")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False  # Set to True if you want the keyboard to disappear after a button press
)

async def is_subscribed(bot, query):
    channel = []
    if AUTH_CHANNEL:
        channel.append(AUTH_CHANNEL)
    if SECOND_AUTH_CHANNEL:
        channel.append(SECOND_AUTH_CHANNEL)
    btn = []
    if REQUEST_TO_JOIN_MODE == True and join_db().isActive():
        try:
            user = await join_db().get_user(query.from_user.id)
            for c in channel:
                if user:
                    for ch in user:
                        if c == ch["chat_id"]: 
                            continue 
                    
                else:
                    try:
                        user_data = await bot.get_chat_member(c, query.from_user.id)
                    except UserNotParticipant:
                        invite_link = await bot.create_chat_invite_link(chat_id=(int(c)), creates_join_request=True)
                        chat = await bot.get_chat(c)
                        btn.append([InlineKeyboardButton(f"Join {chat.title}", url=invite_link.invite_link)])
                        pass
                    except Exception as e:
                        print(e)
                        pass
        except Exception as e:
            print(e)
            pass
    else:
        for c in channel:
            try:
                user_data = await bot.get_chat_member(c, query.from_user.id)
            except UserNotParticipant:
                chat = await bot.get_chat(c)
                btn.append([InlineKeyboardButton(f"Join {chat.title}", url=chat.invite_link)])
                pass
            except Exception as e:
                print(e)
                pass
    return btn

@Client.on_chat_join_request(filters.channel | filters.group)
async def join_reqs(client, join_req: ChatJoinRequest):
    if join_db().isActive():
        user_id = join_req.from_user.id
        chat_id = join_req.chat.id

        await join_db().add_user(
            user_id=user_id,
            chat_id=chat_id
        )

@Client.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(client, message):
    if message.chat.type == enums.ChatType.PRIVATE:
        if not await db.is_user_exist(message.from_user.id):
            await db.add_user(message.from_user.id, message.from_user.first_name)
            await client.send_message(LOG_CHANNEL, LOG_TEXT.format(message.from_user.id, message.from_user.mention))
        FSUB = True
        btn = await is_subscribed(client, message)
        if btn and FSUB == False:
            try:
                if len(message.command) != 2 or message.command[1] == "ok":
                    btn.append([InlineKeyboardButton("✅ ᴊᴏɪɴᴇᴅ ✅", url=f"https://t.me/{temp.U_NAME}?start=ok")])
                else:
                    btn.append([InlineKeyboardButton("✅ ᴊᴏɪɴᴇᴅ ✅", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
                text = "**🕵️ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ᴊᴏɪɴ ᴍʏ ᴀɴʏ ᴄʜᴀɴɴᴇʟ ғɪʀsᴛ ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ᴊᴏɪɴᴇᴅ ʙᴜᴛᴛᴏɴ**"
                await client.send_message(
                    chat_id=message.from_user.id,
                    text=text,
                    reply_markup=InlineKeyboardMarkup(btn),
                    parse_mode=enums.ParseMode.MARKDOWN
                )
                return
            except Exception as e:
                print(e)
                return await message.reply_text("something wrong with force subscribe.")

        if len(message.command) != 2 or message.command[1] == "ok":
            return await message.reply_text(text=f"**Hello {message.from_user.mention} 👋,\n\nI am powerfull adult bot with advance festures.**", reply_markup=keyboard)
  
@Client.on_message(filters.private & filters.text & ~filters.command("start"))
async def handle_message(client, message):
    user_id = message.from_user.id
    me = await client.get_me()
    if message.text == "Get Video":
        if not await db.has_premium_access(user_id):
            plan = await db.get_plan(user_id)
            if plan == False:
                today_date_str = datetime.now().strftime('%Y-%m-%d')
                date = await db.get_date(user_id)
                if date != today_date_str:
                    await db.set_date(user_id, date=today_date_str)
                    used = await db.get_free_used(user_id)
                    if used != 0:
                        files = await get_search_results("Sex")
                        random_file = random.choice(files)
                        msg_id = random_file["msg_id"]
                        k = await client.copy_message(message.from_user.id, FILE_CHANNEL, msg_id, caption=f"**Powered By {me.mention}**\n\n<blockquote>This Message Will Be Deleted In 10 Minutes Due To Copyright Issue So Save It Somewhere.</blockquote>")
                        await db.set_free_used(user_id, free_used=1)
                        await asyncio.sleep(600)
                        await k.delete()
                else:
                    used = await db.get_free_used(user_id)
                    if used <= 5:
                        new_used = used + 1
                        files = await get_search_results("Sex")
                        random_file = random.choice(files)
                        msg_id = random_file["msg_id"]
                        k = await client.copy_message(message.from_user.id, FILE_CHANNEL, msg_id, caption=f"**Powered By {me.mention}**\n\n<blockquote>This Message Will Be Deleted In 10 Minutes Due To Copyright Issue So Save It Somewhere.</blockquote>")
                        await db.set_free_used(user_id, free_used=new_used)
                        await asyncio.sleep(600)
                        await k.delete()
                    else:
                        return await message.reply("Your Daily Quota Exceeded Of 6 Files Per Day. Come Back Tomorrow Or Buy Subscription To Get Unlimited Benefits.")
        else:
            today_date_str = datetime.now().strftime('%Y-%m-%d')
            date = await db.get_date(user_id)
            if date != today_date_str:
                await db.set_date(user_id, date=today_date_str)
                used = await db.get_pre_used(user_id)
                if used != 0:
                    files = await get_search_results("Sex", duration=30)
                    random_file = random.choice(files)
                    msg_id = random_file["msg_id"]
                    k = await client.copy_message(message.from_user.id, FILE_CHANNEL, msg_id, caption=f"**Powered By {me.mention}**\n\n<blockquote>This Message Will Be Deleted In 10 Minutes Due To Copyright Issue So Save It Somewhere.</blockquote>")
                    await db.set_pre_used(user_id, pre_used=1)
                    await asyncio.sleep(600)
                    await k.delete()
            else:
                used = await db.get_pre_used(user_id)
                if used <= 29:
                    new_used = used + 1
                    files = await get_search_results("Sex", duration=30)
                    random_file = random.choice(files)
                    msg_id = random_file["msg_id"]
                    k = await client.copy_message(message.from_user.id, FILE_CHANNEL, msg_id, caption=f"**Powered By {me.mention}**\n\n<blockquote>This Message Will Be Deleted In 10 Minutes Due To Copyright Issue So Save It Somewhere.</blockquote>")
                    await db.set_pre_used(user_id, pre_used=new_used)
                    await asyncio.sleep(600)
                    await k.delete()
                else:
                    return await message.reply("Your Daily Quota Exceeded Of 30 Files Per Day. Come Back Tomorrow. Thanks For Your Support.")
       
            

    if message.text == "Brazzers":
        buttons = [[
            InlineKeyboardButton('Buy Subscription', url='http://t.me/VJ_Botz')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(text=BRA_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML)

    if message.text == "My Plan":
        if not await db.has_premium_access(user_id):
            plan = await db.get_plan(user_id)
            if plan == False:
                p = "Free"
                daily = int(6)
                used = await db.get_free_used(user_id)
                remaining = daily - used
            else:
                p = "Paid"
                daily = int(30)
                used = await db.get_pre_used(user_id)
                remaining = daily - used
        else:
            p = "Paid"
            daily = int(30)
            used = await db.get_pre_used(user_id)
            remaining = daily - used
        await message.reply_text(text=PLAN_TXT.format(message.from_user.mention, message.from_user.id, p, daily, used, daily, remaining),
            parse_mode=enums.ParseMode.HTML)

    if message.text == "Subscription":
        buttons = [[
            InlineKeyboardButton('Owner', url='http://t.me/VJ_Botz')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(text=SUBS_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML)

        
