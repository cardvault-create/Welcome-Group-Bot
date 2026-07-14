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

def get_random_video():
    """Har baar random video - used flag reset karke"""
    videos = load_videos()
    if not videos:
        return None
    
    # Sab videos ko available karo
    for v in videos:
        v["used"] = False
    with open(VIDEO_DB, "w") as f:
        json.dump(videos, f, indent=2)
    
    # Random video select karo
    video = random.choice(videos)
    
    # Mark as used (but will reset next time)
    for v in videos:
        if v["id"] == video["id"]:
            v["used"] = True
    with open(VIDEO_DB, "w") as f:
        json.dump(videos, f, indent=2)
    
    return video

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

# ========== TIME FUNCTIONS ==========
def get_current_time():
    return datetime.now(IST).strftime("%I:%M:%S %p")

def get_current_date():
    return datetime.now(IST).strftime("%B %d, %Y")

# ========== 🔥 PREMIUM STYLED MESSAGES ==========

# ---------- JOIN MESSAGES ----------
JOIN_MESSAGES = [
    """🌟━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌟
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    ✨ **__{user}__** ✨    
┃    🎯 **__JOINED__** ᴛʜᴇ ɢʀᴏᴜᴘ!    
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
🌟━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌟

🎉 **__ᴡᴇʟᴄᴏᴍᴇ__** ᴛᴏ ᴛʜᴇ **__ᴘʀᴇᴍɪᴜᴍ__** ғᴀᴍɪʟʏ! 🏆
💎 **__ʏᴏᴜ'ʀᴇ__** ᴛʜᴇ **__ʙᴇsᴛ__** ᴀᴅᴅɪᴛɪᴏɴ ᴛᴏᴅᴀʏ! 🔥
🌈 **__ɢʟᴀᴅ__** ᴛᴏ ʜᴀᴠᴇ ʏᴏᴜ **__ʜᴇʀᴇ__**! 💫

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 **__ᴛɪᴍᴇ:__** `{time}`
📅 **__ᴅᴀᴛᴇ:__** `{date}`
📊 **__ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs:__** `{members}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""",

    """💫━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💫
╔━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╗
║    🚀 **__{user}__** 🚀    
║    👑 **__ENTERED__** ᴛʜᴇ ᴀʀᴇɴᴀ!    
╚━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╝
💫━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💫

🌟 **__ɴᴇᴡ ᴘʟᴀʏᴇʀ__** ɪɴ ᴛʜᴇ ʜᴏᴜsᴇ! 🎮
⚡️ **__ᴡᴇ'ʀᴇ__** sᴏ **__ᴇxᴄɪᴛᴇᴅ__** ᴛᴏ ʜᴀᴠᴇ ʏᴏᴜ! 💫
🔥 **__ʟᴇᴛ's__** ᴍᴀᴋᴇ **__ᴍᴇᴍᴏʀɪᴇs__** ᴛᴏɢᴇᴛʜᴇʀ! 🎊

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 **__ᴛɪᴍᴇ:__** `{time}`
📅 **__ᴅᴀᴛᴇ:__** `{date}`
📊 **__ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs:__** `{members}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""",

    """🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥
╔━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╗
║    ⭐️ **__{user}__** ⭐️    
║    🎊 **__WELCOME__** ᴀʙᴏᴀʀᴅ!    
╚━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╝
🔥━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔥

🌈 **__ɴᴇᴡ__** ᴍᴇᴍʙᴇʀ **__ᴜɴʟᴏᴄᴋᴇᴅ__**! 🗝️
💫 **__ᴛʜᴇ__** ғᴀᴍɪʟʏ **__ɢʀᴏᴡs__** ʙʏ ᴏɴᴇ! 🎉
💎 **__ʏᴏᴜ'ʀᴇ__** ᴀ **__ᴠᴀʟᴜᴀʙʟᴇ__** ᴀᴅᴅɪᴛɪᴏɴ! 🌟

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 **__ᴛɪᴍᴇ:__** `{time}`
📅 **__ᴅᴀᴛᴇ:__** `{date}`
📊 **__ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs:__** `{members}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""",

    """🌈━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌈
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    🎇 **__{user}__** 🎇    
┃    💫 **__JOINED__** ᴛʜᴇ ᴄʀᴇᴡ!    
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
🌈━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌈

💝 **__ʟᴏᴠᴇ__** ᴛᴏ ʜᴀᴠᴇ ʏᴏᴜ **__ʜᴇʀᴇ__**! 💕
🎵 **__ʟᴇᴛ's__** ᴍᴀᴋᴇ **__ᴍᴇᴍᴏʀɪᴇs__** ᴛᴏɢᴇᴛʜᴇʀ! 🎶
🌟 **__ᴛᴏɢᴇᴛʜᴇʀ__** ᴡᴇ ᴀʀᴇ **__sᴛʀᴏɴɢᴇʀ__**! 💪

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 **__ᴛɪᴍᴇ:__** `{time}`
📅 **__ᴅᴀᴛᴇ:__** `{date}`
📊 **__ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs:__** `{members}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
]

# ---------- LEFT MESSAGES ----------
LEFT_MESSAGES = [
    """😔━━━━━━━━━━━━━━━━━━━━━━━━━━━━━😔
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    💔 **__{user}__** 💔    
┃    🚶 **__LEFT__** ᴛʜᴇ ɢʀᴏᴜᴘ!    
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
😔━━━━━━━━━━━━━━━━━━━━━━━━━━━━━😔

🕊️ **__ᴡᴇ'ʟʟ__** ᴍɪss ʏᴏᴜ **__ᴅᴇᴀʀ__** ғʀɪᴇɴᴅ! 💫
🌈 **__ɢᴏᴏᴅʙʏᴇ__** ᴀɴᴅ **__ᴛᴀᴋᴇ__** ᴄᴀʀᴇ! 🌟
💫 **__ʜᴏᴘᴇ__** ᴛᴏ sᴇᴇ ʏᴏᴜ **__ᴀɢᴀɪɴ__**! 🤞

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 **__ᴛɪᴍᴇ:__** `{time}`
📅 **__ᴅᴀᴛᴇ:__** `{date}`
📊 **__ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs:__** `{members}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""",

    """🌧️━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌧️
╔━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╗
║    👋 **__{user}__** 👋    
║    🚪 **__EXITED__** ᴛʜᴇ ɢʀᴏᴜᴘ!    
╚━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╝
🌧️━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌧️

😢 **__sᴀᴅ__** ᴛᴏ sᴇᴇ ʏᴏᴜ **__ʟᴇᴀᴠᴇ__**! 💔
🌟 **__ʏᴏᴜ'ʟʟ__** ʙᴇ **__ᴍɪssᴇᴅ__** ʜᴇʀᴇ! 🥺
🌈 **__ᴡɪsʜɪɴɢ__** ʏᴏᴜ **__ʙᴇsᴛ__** ғᴏʀ ᴛʜᴇ ғᴜᴛᴜʀᴇ! ✨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 **__ᴛɪᴍᴇ:__** `{time}`
📅 **__ᴅᴀᴛᴇ:__** `{date}`
📊 **__ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs:__** `{members}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""",

    """🌊━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌊
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    💧 **__{user}__** 💧    
┃    🚣 **__SAILED__** ᴀᴡᴀʏ!    
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
🌊━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌊

🌅 **__ᴛʜᴇ__** sᴜɴ sᴇᴛs ᴏɴ **__ʏᴏᴜʀ__** ᴅᴇᴘᴀʀᴛᴜʀᴇ! 🌄
🕊️ **__ᴍᴀʏ__** ʏᴏᴜ **__ғɪɴᴅ__** ᴘᴇᴀᴄᴇ ᴇᴠᴇʀʏᴡʜᴇʀᴇ! ✨
🌟 **__ᴛʜᴀɴᴋ__** ʏᴏᴜ ғᴏʀ ʙᴇɪɴɢ ᴘᴀʀᴛ ᴏғ ᴛʜɪs **__ғᴀᴍɪʟʏ__**! 💫

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 **__ᴛɪᴍᴇ:__** `{time}`
📅 **__ᴅᴀᴛᴇ:__** `{date}`
📊 **__ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs:__** `{members}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
]

# ---------- BAN MESSAGES ----------
BAN_MESSAGES = [
    """🚫━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🚫
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    ⛔️ **__{user}__** ⛔️    
┃    🔨 **__BANNED__** ғʀᴏᴍ ɢʀᴏᴜᴘ!    
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
🚫━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🚫

⚖️ **__ʀᴜʟᴇs__** ᴡᴇʀᴇ **__ʙʀᴏᴋᴇɴ__**! 🚨
❌ **__ᴀᴄᴛɪᴏɴ__** ʜᴀs ʙᴇᴇɴ **__ᴛᴀᴋᴇɴ__**! 💥
🛡️ **__ᴛʜᴇ__** ᴄᴏᴍᴍᴜɴɪᴛʏ ɪs **__sᴀғᴇ__** ɴᴏᴡ! 🎯

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 **__ᴛɪᴍᴇ:__** `{time}`
📅 **__ᴅᴀᴛᴇ:__** `{date}`
📊 **__ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs:__** `{members}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""",

    """🔒━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔒
╔━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╗
║    🚷 **__{user}__** 🚷    
║    🔐 **__PERMANENTLY__** ʙᴀɴɴᴇᴅ!    
╚━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╝
🔒━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🔒

⛓️ **__sᴇᴄᴜʀɪᴛʏ__** ᴍᴇᴀsᴜʀᴇs **__ᴀᴄᴛɪᴠᴀᴛᴇᴅ__**! 🛡️
🗑️ **__ʀᴇᴍᴏᴠᴇᴅ__** ғʀᴏᴍ ᴛʜᴇ **__ᴄᴏᴍᴍᴜɴɪᴛʏ__**! ❌
💀 **__ɴᴏ__** ᴛᴏʟᴇʀᴀɴᴄᴇ ғᴏʀ **__ʀᴜʟᴇ ʙʀᴇᴀᴋᴇʀs__**! ⚡

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 **__ᴛɪᴍᴇ:__** `{time}`
📅 **__ᴅᴀᴛᴇ:__** `{date}`
📊 **__ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs:__** `{members}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""",

    """⚡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⚡
╔━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╗
║    💢 **__{user}__** 💢    
║    ⚔️ **__BANISHED__** ғᴏʀᴇᴠᴇʀ!    
╚━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╝
⚡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⚡

🗡️ **__ᴊᴜsᴛɪᴄᴇ__** ʜᴀs ʙᴇᴇɴ **__sᴇʀᴠᴇᴅ__**! ⚖️
🛡️ **__ᴛʜᴇ__** ɢʀᴏᴜᴘ ɪs **__sᴀғᴇ__** ᴀɢᴀɪɴ! 🎯
🌟 **__ʀᴜʟᴇs__** ᴀʀᴇ **__ɴᴏɴ-ɴᴇɢᴏᴛɪᴀʙʟᴇ__**! 💪

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕐 **__ᴛɪᴍᴇ:__** `{time}`
📅 **__ᴅᴀᴛᴇ:__** `{date}`
📊 **__ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs:__** `{members}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
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

# ========== GET MEMBER COUNT ==========
async def get_member_count(chat_id):
    try:
        chat = await app.get_chat(chat_id)
        return chat.members_count
    except:
        return "?"

# ========== SEND PREMIUM NOTIFICATION ==========
async def send_premium_notification(chat_id, user_mention, message_template, event_type):
    try:
        time = get_current_time()
        date = get_current_date()
        members = await get_member_count(chat_id)
        
        msg_text = message_template.format(
            user=user_mention,
            time=time,
            date=date,
            members=members
        )
        
        # Premium footer with random emojis
        emojis = ["🔥", "✨", "💎", "🌟", "🎉", "🚀", "👑", "💫", "⭐️", "🌈", "⚡️", "💥", "🎊", "🏆", "❤️"]
        footer = random.sample(emojis, 4)
        msg_text += f"\n\n{footer[0]} **__ᴘʀᴇᴍɪᴜᴍ__** {footer[1]} **__ᴜᴘᴅᴀᴛᴇ__** {footer[2]} **__ʙʏ__** {footer[3]} **__ʙᴏᴛ__**"
        
        # Get random video - HAR BAAR NAYI VIDEO
        video_data = get_random_video()
        
        if video_data and os.path.exists(video_data["path"]):
            await app.send_video(
                chat_id=chat_id,
                video=video_data["path"],
                caption=msg_text,
                supports_streaming=True,
                width=1920,
                height=1080
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
        confirm_text = f"""✅━━━━━━━━━━━━━━━━━━━━━━━━━━━━━✅
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    **__ɢʀᴏᴜᴘ ᴀᴅᴅᴇᴅ__** 🎉    
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
✅━━━━━━━━━━━━━━━━━━━━━━━━━━━━━✅

📛 **__ɴᴀᴍᴇ:__** `{chat_name}`
🆔 **__ɪᴅ:__** `{chat_id}`
🕐 **__ᴛɪᴍᴇ:__** `{get_current_time()}`
📅 **__ᴅᴀᴛᴇ:__** `{get_current_date()}`

🌟 **__sᴛᴀᴛᴜs:__** ✅ **__ᴀᴄᴛɪᴠᴇ__**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 **__ᴘʀᴇᴍɪᴜᴍ__** **__ᴇɴᴀʙʟᴇᴅ__** 💎
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡️ **__ɴᴏᴡ ᴍᴏɴɪᴛᴏʀɪɴɢ:__**
• 👤 **__Jᴏɪɴs__** 
• 🚶 **__Lᴇᴀᴠᴇs__**
• 🚫 **__Bᴀɴs__**

📹 **__ᴠɪᴅᴇᴏs__** **__ʟᴏᴀᴅᴇᴅ:__** `{get_video_count()}`"""

        # Send confirmation
        sent_msg = await message.reply_text(confirm_text)
        
        # Auto-delete after 5 seconds
        await asyncio.sleep(5)
        try:
            await sent_msg.delete()
            await message.delete()
        except:
            pass
        
        logger.info(f"✅ Group auto-added: {chat_name} ({chat_id})")
        
    except Exception as e:
        await message.reply_text(f"❌ **__ᴇʀʀᴏʀ:__** {str(e)}")
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
            if hasattr(message, 'new_chat_members') and message.new_chat_members is None:
                await send_premium_notification(
                    chat_id,
                    mention,
                    random.choice(BAN_MESSAGES),
                    "BAN"
                )
                logger.info(f"🚫 BANNED: {user.first_name} in {chat_id}")
            else:
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
        await message.reply_text("❌ **__ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇss!__**")
        return
    
    await message.reply_text(
        f"""🌟━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌟
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    **__ᴘʀᴇᴍɪᴜᴍ ɢʀᴏᴜᴘ ʙᴏᴛ__**    
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
🌟━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🌟

**__ʜᴇʏ__** {message.from_user.first_name}! 👋

✅ **__ʙᴏᴛ__** ɪs **__ᴡᴏʀᴋɪɴɢ__** ᴘʀᴏᴘᴇʀʟʏ!

📹 **__ᴛᴏᴛᴀʟ ᴠɪᴅᴇᴏs:__** `{get_video_count()}`
👥 **__ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘs:__** `{len(get_all_groups())}`

**__ᴄᴏᴍᴍᴀɴᴅs:__**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📹 **__ᴠɪᴅᴇᴏ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ__**
• `/addvideo` - **__ᴀᴅᴅ__** ᴠɪᴅᴇᴏ
• `/videos` - **__ᴠɪᴇᴡ__** ᴀʟʟ
• `/delvideo` - **__ᴅᴇʟᴇᴛᴇ__**
• `/clearvideos` - **__ᴄʟᴇᴀʀ__** ᴀʟʟ

👥 **__ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ__**
• `/addgroup` - **__ᴀᴅᴅ__** ɢʀᴏᴜᴘ
• `/groups` - **__ᴠɪᴇᴡ__** ᴀʟʟ
• `/delgroup` - **__ʀᴇᴍᴏᴠᴇ__**
• `/toggle` - **__ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ__**

📊 **__sᴛᴀᴛɪsᴛɪᴄs__**
• `/stats` - **__ʙᴏᴛ__** sᴛᴀᴛs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 **__ᴘʀᴇᴍɪᴜᴍ__** **__ʙᴏᴛ__** 💎
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    )

@app.on_message(filters.command("addgroup") & filters.private)
async def add_group_private(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply_text(
                "❌ **__ᴜsᴀɢᴇ:__** `/addgroup -100123456789`\n\n"
                "📌 **__ᴛɪᴘ:__** ɢʀᴏᴜᴘ ᴍᴇɪɴ `/addgroup` ᴛʏᴘᴇ ᴋᴀʀᴏ ᴀᴜᴛᴏ-ᴀᴅᴅ ʜᴏ ɢᴀʏᴇɢᴀ!"
            )
            return
        
        group_id = int(parts[1])
        group_name = parts[2] if len(parts) > 2 else f"Group {group_id}"
        
        save_group(group_id, group_name)
        await message.reply_text(
            f"✅ **__ɢʀᴏᴜᴘ ᴀᴅᴅᴇᴅ!__** 🎉\n\n"
            f"📛 **__ɴᴀᴍᴇ:__** `{group_name}`\n"
            f"🆔 **__ɪᴅ:__** `{group_id}`"
        )
    except Exception as e:
        await message.reply_text(f"❌ **__ᴇʀʀᴏʀ:__** {str(e)}")

@app.on_message(filters.command("groups") & filters.private)
async def groups_list(client, message):
    if not is_owner(message.from_user.id):
        return
    
    groups = get_all_groups()
    if not groups:
        await message.reply_text("❌ **__ɴᴏ ɢʀᴏᴜᴘs ᴀᴅᴅᴇᴅ!__**")
        return
    
    text = "👥 **__ᴍʏ ɢʀᴏᴜᴘs__**\n\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    for group_id, data in groups.items():
        status = "✅" if data.get("enabled", True) else "❌"
        text += f"{status} **__{data['name']}__**\n"
        text += f"   🆔 `{group_id}`\n"
        text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    await message.reply_text(text)

@app.on_message(filters.command("delgroup") & filters.private)
async def delete_group(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text("❌ **__ᴜsᴀɢᴇ:__** `/delgroup -100123456789`")
            return
        
        group_id = int(parts[1])
        if remove_group(group_id):
            await message.reply_text(f"✅ **__ɢʀᴏᴜᴘ ʀᴇᴍᴏᴠᴇᴅ!__**")
        else:
            await message.reply_text(f"❌ **__ɢʀᴏᴜᴘ ɴᴏᴛ ғᴏᴜɴᴅ!__**")
    except:
        await message.reply_text("❌ **__ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ!__**")

@app.on_message(filters.command("toggle") & filters.private)
async def toggle_group_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text("❌ **__ᴜsᴀɢᴇ:__** `/toggle -100123456789`")
            return
        
        group_id = int(parts[1])
        status = toggle_group(group_id)
        await message.reply_text(
            f"✅ **__ɢʀᴏᴜᴘ ᴛᴏɢɢʟᴇᴅ!__**\n\n"
            f"🆔 `{group_id}`\n"
            f"📊 **__sᴛᴀᴛᴜs:__** {'✅ ᴇɴᴀʙʟᴇᴅ' if status else '❌ ᴅɪsᴀʙʟᴇᴅ'}"
        )
    except:
        await message.reply_text("❌ **__ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ!__**")

@app.on_message(filters.command("addvideo") & filters.private)
async def add_video_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    status = await message.reply_text("⏳ **__ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...__**")
    
    try:
        if message.reply_to_message and message.reply_to_message.video:
            video_path = await message.reply_to_message.download()
            video_id = save_video(video_path)
            await status.edit_text(
                f"✅ **__ᴠɪᴅᴇᴏ #`{video_id}` sᴀᴠᴇᴅ!__** 🎉\n\n"
                f"📹 **__ᴛᴏᴛᴀʟ:__** `{get_video_count()}`"
            )
        else:
            await status.edit_text(
                "❌ **__ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ!__**\n\n"
                "**__ᴜsᴀɢᴇ:__** Send video → Reply with `/addvideo`"
            )
    except Exception as e:
        await status.edit_text(f"❌ **__ᴇʀʀᴏʀ:__** {str(e)}")

@app.on_message(filters.command("videos") & filters.private)
async def list_videos(client, message):
    if not is_owner(message.from_user.id):
        return
    
    videos = load_videos()
    if not videos:
        await message.reply_text("❌ **__ɴᴏ ᴠɪᴅᴇᴏs ғᴏᴜɴᴅ!__**")
        return
    
    text = "🎬 **__ᴠɪᴅᴇᴏ ʟɪʙʀᴀʀʏ__**\n\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    for video in videos:
        used = "✅" if video.get("used", False) else "🔄"
        text += f"{used} **#`{video['id']}`** {video['name']}\n"
        text += f"   🕐 `{video['timestamp'][:16]}`\n"
        text += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    text += f"\n📹 **__ᴛᴏᴛᴀʟ:__** `{len(videos)}`"
    await message.reply_text(text)

@app.on_message(filters.command("delvideo") & filters.private)
async def delete_video_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text("❌ **__ᴜsᴀɢᴇ:__** `/delvideo 1`")
            return
        
        video_id = int(parts[1])
        if delete_video_by_id(video_id):
            await message.reply_text(f"✅ **__ᴠɪᴅᴇᴏ #`{video_id}` ᴅᴇʟᴇᴛᴇᴅ!__**")
        else:
            await message.reply_text(f"❌ **__ᴠɪᴅᴇᴏ #`{video_id}` ɴᴏᴛ ғᴏᴜɴᴅ!__**")
    except:
        await message.reply_text("❌ **__ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ!__**")

@app.on_message(filters.command("clearvideos") & filters.private)
async def clear_videos_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    videos = load_videos()
    if not videos:
        await message.reply_text("❌ **__ɴᴏ ᴠɪᴅᴇᴏs ᴛᴏ ᴄʟᴇᴀʀ!__**")
        return
    
    for video in videos:
        if os.path.exists(video["path"]):
            os.remove(video["path"])
    
    with open(VIDEO_DB, "w") as f:
        json.dump([], f)
    
    await message.reply_text(f"🗑️ **__ᴀʟʟ {len(videos)} ᴠɪᴅᴇᴏs ᴄʟᴇᴀʀᴇᴅ!__**")

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
    
    text = f"""📊 **__ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs__**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📹 **__ᴛᴏᴛᴀʟ ᴠɪᴅᴇᴏs:__** `{len(videos)}`
🔄 **__ᴜɴᴜsᴇᴅ:__** `{len(videos) - used}`
✅ **__ᴜsᴇᴅ:__** `{used}`
💾 **__ᴛᴏᴛᴀʟ sɪᴢᴇ:__** `{total_size / (1024*1024):.2f} MB`

👥 **__ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘs:__** `{len(groups)}`
✅ **__ᴇɴᴀʙʟᴇᴅ:__** `{sum(1 for g in groups.values() if g.get('enabled', True))}`

⏰ **__ᴜᴘᴛɪᴍᴇ:__** `{datetime.now(IST).strftime('%B %d, %Y %I:%M %p')}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 **__ᴘʀᴇᴍɪᴜᴍ__** **__ʙᴏᴛ__** 💎
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    
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
    print("📌 HAR BAAR NAYI VIDEO AAYEGI!")
    print("="*60 + "\n")
    
    try:
        app.run()
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
