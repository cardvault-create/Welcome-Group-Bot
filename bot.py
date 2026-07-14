import asyncio
import json
import random
import os
import logging
from datetime import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import Message

# ========== LOGGING ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== 🔴 YAHAN APNA DATA DAALO ==========
API_ID = 35140329  # 🔴 my.telegram.org se
API_HASH = "011f638e4acadee178c59afffc80193d"  # 🔴 my.telegram.org se
BOT_TOKEN = "8603632286:AAE8Hw5xWzKjrpr4r7PrrMifZxu7-v93TaM"  # 🔴 @BotFather se
OWNER_ID = 7614459746  # 🔴 APNA TELEGRAM USER ID

# ========== DATABASE ==========
VIDEO_DB = "videos.json"
GROUPS_DB = "groups.json"

# ========== TIMEZONE ==========
IST = pytz.timezone('Asia/Kolkata')

# ========== DATABASE FUNCTIONS ==========
def load_videos():
    try:
        if os.path.exists(VIDEO_DB):
            with open(VIDEO_DB, "r") as f:
                return json.load(f)
    except:
        pass
    return []

def save_video(video_path):
    videos = load_videos()
    video_id = len(videos) + 1
    videos.append({
        "id": video_id,
        "path": video_path,
        "timestamp": datetime.now(IST).isoformat(),
        "used": False,
        "name": os.path.basename(video_path)
    })
    with open(VIDEO_DB, "w") as f:
        json.dump(videos, f, indent=2)
    logger.info(f"✅ Video #{video_id} saved")
    return video_id

def get_unused_video():
    videos = load_videos()
    if not videos:
        return None
    
    unused = [v for v in videos if not v.get("used", False)]
    if unused:
        video = random.choice(unused)
        for v in videos:
            if v["id"] == video["id"]:
                v["used"] = True
        with open(VIDEO_DB, "w") as f:
            json.dump(videos, f, indent=2)
        return video
    
    for v in videos:
        v["used"] = False
    with open(VIDEO_DB, "w") as f:
        json.dump(videos, f, indent=2)
    return random.choice(videos)

def get_video_count():
    return len(load_videos())

def delete_video_by_id(video_id):
    videos = load_videos()
    for i, video in enumerate(videos):
        if video["id"] == video_id:
            deleted = videos.pop(i)
            if os.path.exists(deleted["path"]):
                os.remove(deleted["path"])
            with open(VIDEO_DB, "w") as f:
                json.dump(videos, f, indent=2)
            return True
    return False

def load_groups():
    try:
        if os.path.exists(GROUPS_DB):
            with open(GROUPS_DB, "r") as f:
                return json.load(f)
    except:
        pass
    return {}

def save_group(group_id, group_name):
    groups = load_groups()
    groups[str(group_id)] = {
        "name": group_name,
        "added_at": datetime.now(IST).isoformat(),
        "enabled": True
    }
    with open(GROUPS_DB, "w") as f:
        json.dump(groups, f, indent=2)

def remove_group(group_id):
    groups = load_groups()
    if str(group_id) in groups:
        del groups[str(group_id)]
        with open(GROUPS_DB, "w") as f:
            json.dump(groups, f, indent=2)
        return True
    return False

def get_all_groups():
    return load_groups()

def is_group_enabled(group_id):
    groups = load_groups()
    return str(group_id) in groups and groups[str(group_id)].get("enabled", True)

def toggle_group(group_id):
    groups = load_groups()
    if str(group_id) in groups:
        groups[str(group_id)]["enabled"] = not groups[str(group_id)].get("enabled", True)
        with open(GROUPS_DB, "w") as f:
            json.dump(groups, f, indent=2)
        return groups[str(group_id)]["enabled"]
    return False

# ========== PREMIUM MESSAGES ==========
def get_current_time():
    return datetime.now(IST).strftime("%I:%M:%S %p")

def get_current_date():
    return datetime.now(IST).strftime("%B %d, %Y")

JOIN_MESSAGES = [
    """🌟━━━━━━━━━━━━━━━━━━━━━━━🌟
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ✨ **{user}** ✨
┃ 🎯 **JOINED** the group!
┗━━━━━━━━━━━━━━━━━━━━━━━┛
🌟━━━━━━━━━━━━━━━━━━━━━━━🌟

🎉 **ᴡᴇʟᴄᴏᴍᴇ** ᴛᴏ ᴛʜᴇ **ᴘʀᴇᴍɪᴜᴍ** ғᴀᴍɪʟʏ! 🏆
💎 **ʏᴏᴜ'ʀᴇ** ᴛʜᴇ **ʙᴇsᴛ** ᴀᴅᴅɪᴛɪᴏɴ ᴛᴏᴅᴀʏ! 🔥

━━━━━━━━━━━━━━━━━━━━━━━
🕐 **ᴛɪᴍᴇ:** `{time}`
📅 **ᴅᴀᴛᴇ:** `{date}`
━━━━━━━━━━━━━━━━━━━━━━━""",

    """💫━━━━━━━━━━━━━━━━━━━━━━━💫
╔━━━━━━━━━━━━━━━━━━━━━━━╗
║ 🚀 **{user}** 🚀
║ 👑 **ENTERED** the arena!
╚━━━━━━━━━━━━━━━━━━━━━━━╝
💫━━━━━━━━━━━━━━━━━━━━━━━💫

🌟 **ɴᴇᴡ ᴘʟᴀʏᴇʀ** ɪɴ ᴛʜᴇ ʜᴏᴜsᴇ! 🎮
⚡️ **ᴡᴇ'ʀᴇ** sᴏ **ᴇxᴄɪᴛᴇᴅ** ᴛᴏ ʜᴀᴠᴇ ʏᴏᴜ! 💫

━━━━━━━━━━━━━━━━━━━━━━━
🕐 **ᴛɪᴍᴇ:** `{time}`
📅 **ᴅᴀᴛᴇ:** `{date}`
━━━━━━━━━━━━━━━━━━━━━━━"""
]

LEFT_MESSAGES = [
    """😔━━━━━━━━━━━━━━━━━━━━━━━😔
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 💔 **{user}** 💔
┃ 🚶 **LEFT** the group!
┗━━━━━━━━━━━━━━━━━━━━━━━┛
😔━━━━━━━━━━━━━━━━━━━━━━━😔

🕊️ **ᴡᴇ'ʟʟ** ᴍɪss ʏᴏᴜ **ᴅᴇᴀʀ** ғʀɪᴇɴᴅ! 💫
🌈 **ɢᴏᴏᴅʙʏᴇ** ᴀɴᴅ **ᴛᴀᴋᴇ** ᴄᴀʀᴇ! 🌟

━━━━━━━━━━━━━━━━━━━━━━━
🕐 **ᴛɪᴍᴇ:** `{time}`
📅 **ᴅᴀᴛᴇ:** `{date}`
━━━━━━━━━━━━━━━━━━━━━━━"""
]

BAN_MESSAGES = [
    """🚫━━━━━━━━━━━━━━━━━━━━━━━🚫
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ⛔️ **{user}** ⛔️
┃ 🔨 **BANNED** from group!
┗━━━━━━━━━━━━━━━━━━━━━━━┛
🚫━━━━━━━━━━━━━━━━━━━━━━━🚫

⚖️ **ʀᴜʟᴇs** ᴡᴇʀᴇ **ʙʀᴏᴋᴇɴ**! 🚨
❌ **ᴀᴄᴛɪᴏɴ** ʜᴀs ʙᴇᴇɴ **ᴛᴀᴋᴇɴ**! 💥

━━━━━━━━━━━━━━━━━━━━━━━
🕐 **ᴛɪᴍᴇ:** `{time}`
📅 **ᴅᴀᴛᴇ:** `{date}`
━━━━━━━━━━━━━━━━━━━━━━━"""
]

# ========== BOT CREATE ==========
print("🔧 Creating bot...")

app = Client(
    "premium_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("✅ Bot created!")

# ========== OWNER CHECK ==========
def is_owner(user_id):
    return user_id == OWNER_ID

# ========== SEND PREMIUM NOTIFICATION ==========
async def send_premium_notification(chat_id, user_mention, message_template, event_type):
    try:
        time = get_current_time()
        date = get_current_date()
        
        msg_text = message_template.format(
            user=user_mention,
            time=time,
            date=date
        )
        
        emojis = ["🔥", "✨", "💎", "🌟", "🎉", "🚀", "👑", "💫"]
        footer = random.sample(emojis, 3)
        msg_text += f"\n\n{footer[0]} **ᴘʀᴇᴍɪᴜᴍ** {footer[1]} **ᴜᴘᴅᴀᴛᴇ** {footer[2]}"
        
        video_data = get_unused_video()
        
        if video_data and os.path.exists(video_data["path"]):
            await app.send_video(
                chat_id=chat_id,
                video=video_data["path"],
                caption=msg_text,
                supports_streaming=True
            )
            logger.info(f"📹 Video #{video_data['id']} sent to {chat_id}")
        else:
            await app.send_message(chat_id=chat_id, text=msg_text)
            logger.info(f"📝 Message sent to {chat_id} (no video)")
    except Exception as e:
        logger.error(f"❌ Error: {e}")

# ========== 🔴 GROUP AUTO-ADD HANDLER ==========
@app.on_message(filters.group & filters.command("addgroup") & filters.user(OWNER_ID))
async def add_group_from_group(client, message: Message):
    try:
        chat_id = message.chat.id
        chat_name = message.chat.title or f"Group {chat_id}"
        
        # Save group
        save_group(chat_id, chat_name)
        
        # Premium confirmation message
        confirm_text = f"""✅━━━━━━━━━━━━━━━━━━━━━━━✅
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃ **ɢʀᴏᴜᴘ ᴀᴅᴅᴇᴅ** 🎉
┗━━━━━━━━━━━━━━━━━━━━━━━┛
✅━━━━━━━━━━━━━━━━━━━━━━━✅

📛 **ɴᴀᴍᴇ:** `{chat_name}`
🆔 **ɪᴅ:** `{chat_id}`
📅 **ᴛɪᴍᴇ:** `{get_current_time()}`
📆 **ᴅᴀᴛᴇ:** `{get_current_date()}`

🌟 **sᴛᴀᴛᴜs:** ✅ ᴀᴄᴛɪᴠᴇ

━━━━━━━━━━━━━━━━━━━━━━━
💎 **ᴘʀᴇᴍɪᴜᴍ** ᴇɴᴀʙʟᴇᴅ 💎
━━━━━━━━━━━━━━━━━━━━━━━

⚡️ **ɴᴏᴡ ᴍᴏɴɪᴛᴏʀɪɴɢ:**
• 👤 Jᴏɪɴs
• 🚶 Lᴇᴀᴠᴇs
• 🚫 Bᴀɴs"""

        # Send confirmation
        sent_msg = await message.reply_text(confirm_text)
        
        # Auto-delete after 5 seconds
        await asyncio.sleep(5)
        try:
            await sent_msg.delete()
            await message.delete()  # Delete command message too
        except:
            pass
        
        logger.info(f"✅ Group auto-added: {chat_name} ({chat_id})")
        
    except Exception as e:
        await message.reply_text(f"❌ **ᴇʀʀᴏʀ:** {str(e)}")
        logger.error(f"❌ Error in group add: {e}")

# ========== 🔴 SERVICE MESSAGES HANDLER ==========
@app.on_message(filters.group & filters.service)
async def service_message_handler(client, message: Message):
    try:
        chat_id = message.chat.id
        
        # Check if group is enabled
        if not is_group_enabled(chat_id):
            return
        
        # Check for new chat members (JOIN)
        if message.new_chat_members:
            for user in message.new_chat_members:
                if user.is_bot:
                    continue
                mention = f"[{user.first_name}](tg://user?id={user.id})"
                await send_premium_notification(
                    chat_id,
                    mention,
                    random.choice(JOIN_MESSAGES),
                    "JOIN"
                )
                logger.info(f"👤 JOIN: {user.first_name} in {chat_id}")
        
        # Check for left chat member (LEFT or BAN)
        elif message.left_chat_member:
            user = message.left_chat_member
            if user.is_bot:
                return
                
            mention = f"[{user.first_name}](tg://user?id={user.id})"
            
            # Check if user was kicked (banned)
            # In service messages, if someone is banned, the message type is different
            if hasattr(message, 'new_chat_members') and message.new_chat_members is None:
                # This is a ban/kick
                await send_premium_notification(
                    chat_id,
                    mention,
                    random.choice(BAN_MESSAGES),
                    "BAN"
                )
                logger.info(f"🚫 BANNED: {user.first_name} in {chat_id}")
            else:
                # Normal left
                await send_premium_notification(
                    chat_id,
                    mention,
                    random.choice(LEFT_MESSAGES),
                    "LEFT"
                )
                logger.info(f"🚶 LEFT: {user.first_name} in {chat_id}")
                
    except Exception as e:
        logger.error(f"❌ Error in service handler: {e}")

# ========== COMMANDS ==========

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    if not is_owner(message.from_user.id):
        await message.reply_text("❌ **ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇss!**")
        return
    
    await message.reply_text(
        f"""🌟━━━━━━━━━━━━━━━━━━━━━━━🌟
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃ **ᴘʀᴇᴍɪᴜᴍ ɢʀᴏᴜᴘ ʙᴏᴛ** ┃
┗━━━━━━━━━━━━━━━━━━━━━━━┛
🌟━━━━━━━━━━━━━━━━━━━━━━━🌟

**ʜᴇʏ** {message.from_user.first_name}! 👋

✅ Bot is **working** properly!

📹 **ᴛᴏᴛᴀʟ ᴠɪᴅᴇᴏs:** `{get_video_count()}`
👥 **ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘs:** `{len(get_all_groups())}`

**ᴄᴏᴍᴍᴀɴᴅs:**
━━━━━━━━━━━━━━━━━━━━━━━
📹 **ᴠɪᴅᴇᴏ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ**
• `/addvideo` - ᴀᴅᴅ ᴠɪᴅᴇᴏ
• `/videos` - ᴠɪᴇᴡ ᴀʟʟ
• `/delvideo` - ᴅᴇʟᴇᴛᴇ
• `/clearvideos` - ᴄʟᴇᴀʀ ᴀʟʟ

👥 **ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ**
• `/addgroup` - ᴀᴅᴅ ɢʀᴏᴜᴘ
• `/groups` - ᴠɪᴇᴡ ᴀʟʟ
• `/delgroup` - ʀᴇᴍᴏᴠᴇ
• `/toggle` - ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ

📊 **sᴛᴀᴛɪsᴛɪᴄs**
• `/stats` - ʙᴏᴛ sᴛᴀᴛs

━━━━━━━━━━━━━━━━━━━━━━━
💎 **ᴘʀᴇᴍɪᴜᴍ** ʙᴏᴛ 💎
━━━━━━━━━━━━━━━━━━━━━━━"""
    )

@app.on_message(filters.command("addgroup") & filters.private)
async def add_group_private(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply_text(
                "❌ **ᴜsᴀɢᴇ:** `/addgroup -100123456789`\n\n"
                "📌 **ᴛɪᴘ:** ɢʀᴏᴜᴘ ᴍᴇɪɴ `/addgroup` ᴛʏᴘᴇ ᴋᴀʀᴏ ᴀᴜᴛᴏ-ᴀᴅᴅ ʜᴏ ɢᴀʏᴇɢᴀ!"
            )
            return
        
        group_id = int(parts[1])
        group_name = parts[2] if len(parts) > 2 else f"Group {group_id}"
        
        save_group(group_id, group_name)
        await message.reply_text(
            f"✅ **ɢʀᴏᴜᴘ ᴀᴅᴅᴇᴅ!** 🎉\n\n"
            f"📛 **ɴᴀᴍᴇ:** `{group_name}`\n"
            f"🆔 **ɪᴅ:** `{group_id}`"
        )
    except Exception as e:
        await message.reply_text(f"❌ **ᴇʀʀᴏʀ:** {str(e)}")

@app.on_message(filters.command("groups") & filters.private)
async def groups_list(client, message):
    if not is_owner(message.from_user.id):
        return
    
    groups = get_all_groups()
    if not groups:
        await message.reply_text("❌ **ɴᴏ ɢʀᴏᴜᴘs ᴀᴅᴅᴇᴅ!**")
        return
    
    text = "👥 **ᴍʏ ɢʀᴏᴜᴘs**\n\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━\n"
    for group_id, data in groups.items():
        status = "✅" if data.get("enabled", True) else "❌"
        text += f"{status} **{data['name']}**\n"
        text += f"   🆔 `{group_id}`\n"
        text += "━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    await message.reply_text(text)

@app.on_message(filters.command("delgroup") & filters.private)
async def delete_group(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text("❌ **ᴜsᴀɢᴇ:** `/delgroup -100123456789`")
            return
        
        group_id = int(parts[1])
        if remove_group(group_id):
            await message.reply_text(f"✅ **ɢʀᴏᴜᴘ ʀᴇᴍᴏᴠᴇᴅ!**")
        else:
            await message.reply_text(f"❌ **ɢʀᴏᴜᴘ ɴᴏᴛ ғᴏᴜɴᴅ!**")
    except:
        await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ!**")

@app.on_message(filters.command("toggle") & filters.private)
async def toggle_group_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text("❌ **ᴜsᴀɢᴇ:** `/toggle -100123456789`")
            return
        
        group_id = int(parts[1])
        status = toggle_group(group_id)
        await message.reply_text(
            f"✅ **ɢʀᴏᴜᴘ ᴛᴏɢɢʟᴇᴅ!**\n\n"
            f"🆔 `{group_id}`\n"
            f"📊 **sᴛᴀᴛᴜs:** {'✅ ᴇɴᴀʙʟᴇᴅ' if status else '❌ ᴅɪsᴀʙʟᴇᴅ'}"
        )
    except:
        await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ!**")

@app.on_message(filters.command("addvideo") & filters.private)
async def add_video_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    status = await message.reply_text("⏳ **ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...**")
    
    try:
        if message.reply_to_message and message.reply_to_message.video:
            video_path = await message.reply_to_message.download()
            video_id = save_video(video_path)
            await status.edit_text(
                f"✅ **ᴠɪᴅᴇᴏ #`{video_id}` sᴀᴠᴇᴅ!** 🎉\n\n"
                f"📹 **ᴛᴏᴛᴀʟ:** `{get_video_count()}`"
            )
        else:
            await status.edit_text(
                "❌ **ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ!**\n\n"
                "**ᴜsᴀɢᴇ:** Send video → Reply with `/addvideo`"
            )
    except Exception as e:
        await status.edit_text(f"❌ **ᴇʀʀᴏʀ:** {str(e)}")

@app.on_message(filters.command("videos") & filters.private)
async def list_videos(client, message):
    if not is_owner(message.from_user.id):
        return
    
    videos = load_videos()
    if not videos:
        await message.reply_text("❌ **ɴᴏ ᴠɪᴅᴇᴏs ғᴏᴜɴᴅ!**")
        return
    
    text = "🎬 **ᴠɪᴅᴇᴏ ʟɪʙʀᴀʀʏ**\n\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━\n"
    for video in videos:
        used = "✅" if video.get("used", False) else "🔄"
        text += f"{used} **#`{video['id']}`** {video['name']}\n"
        text += f"   🕐 `{video['timestamp'][:16]}`\n"
        text += "━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    text += f"\n📹 **ᴛᴏᴛᴀʟ:** `{len(videos)}`"
    await message.reply_text(text)

@app.on_message(filters.command("delvideo") & filters.private)
async def delete_video_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text("❌ **ᴜsᴀɢᴇ:** `/delvideo 1`")
            return
        
        video_id = int(parts[1])
        if delete_video_by_id(video_id):
            await message.reply_text(f"✅ **ᴠɪᴅᴇᴏ #`{video_id}` ᴅᴇʟᴇᴛᴇᴅ!**")
        else:
            await message.reply_text(f"❌ **ᴠɪᴅᴇᴏ #`{video_id}` ɴᴏᴛ ғᴏᴜɴᴅ!**")
    except:
        await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ!**")

@app.on_message(filters.command("clearvideos") & filters.private)
async def clear_videos_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    videos = load_videos()
    if not videos:
        await message.reply_text("❌ **ɴᴏ ᴠɪᴅᴇᴏs ᴛᴏ ᴄʟᴇᴀʀ!**")
        return
    
    for video in videos:
        if os.path.exists(video["path"]):
            os.remove(video["path"])
    
    with open(VIDEO_DB, "w") as f:
        json.dump([], f)
    
    await message.reply_text(f"🗑️ **ᴀʟʟ {len(videos)} ᴠɪᴅᴇᴏs ᴄʟᴇᴀʀᴇᴅ!**")

@app.on_message(filters.command("stats") & filters.private)
async def stats_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    videos = load_videos()
    total_size = 0
    used = 0
    
    for video in videos:
        if os.path.exists(video["path"]):
            total_size += os.path.getsize(video["path"])
        if video.get("used", False):
            used += 1
    
    groups = get_all_groups()
    
    text = f"""📊 **ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs**

━━━━━━━━━━━━━━━━━━━━━━━
📹 **ᴛᴏᴛᴀʟ ᴠɪᴅᴇᴏs:** `{len(videos)}`
🔄 **ᴜɴᴜsᴇᴅ:** `{len(videos) - used}`
✅ **ᴜsᴇᴅ:** `{used}`
💾 **ᴛᴏᴛᴀʟ sɪᴢᴇ:** `{total_size / (1024*1024):.2f} MB`

👥 **ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘs:** `{len(groups)}`
✅ **ᴇɴᴀʙʟᴇᴅ:** `{sum(1 for g in groups.values() if g.get('enabled', True))}`

⏰ **ᴜᴘᴛɪᴍᴇ:** `{datetime.now(IST).strftime('%B %d, %Y %I:%M %p')}`
━━━━━━━━━━━━━━━━━━━━━━━
💎 **ᴘʀᴇᴍɪᴜᴍ** ʙᴏᴛ 💎
━━━━━━━━━━━━━━━━━━━━━━━"""
    
    await message.reply_text(text)

# ========== RUN ==========
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 STARTING PREMIUM BOT...")
    print("="*60 + "\n")
    
    # Create databases
    if not os.path.exists(VIDEO_DB):
        with open(VIDEO_DB, "w") as f:
            json.dump([], f)
    
    if not os.path.exists(GROUPS_DB):
        with open(GROUPS_DB, "w") as f:
            json.dump({}, f)
    
    os.makedirs("downloads", exist_ok=True)
    
    print("📁 Databases created!")
    print(f"📹 Total videos: {get_video_count()}")
    print(f"👥 Total groups: {len(get_all_groups())}")
    print("\n" + "="*60)
    print("🤖 BOT IS RUNNING!")
    print("="*60 + "\n")
    
    try:
        app.run()
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
