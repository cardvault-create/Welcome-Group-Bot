import asyncio
import json
import random
import os
import logging
from datetime import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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
    videos = load_videos()
    if not videos:
        return None
    
    for v in videos:
        v["used"] = False
    with open(VIDEO_DB, "w") as f:
        json.dump(videos, f, indent=2)
    
    video = random.choice(videos)
    
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

# ========== PREMIUM MESSAGES ==========

# ---------- JOIN MESSAGES (10) ----------
JOIN_MESSAGES = [
    """👑━━━━━━━━━━━━━━━━━━━━━━━👑
   🦁 {user} 🦁
   𝐊𝐈𝐍𝐆 𝐖𝐄𝐋𝐂𝐎𝐌𝐄!
👑━━━━━━━━━━━━━━━━━━━━━━━👑

𝐓𝐡𝐞 𝐤𝐢𝐧𝐠 𝐡𝐚𝐬 𝐚𝐫𝐫𝐢𝐯𝐞𝐝! 👑
𝐘𝐨𝐮'𝐫𝐞 𝐭𝐡𝐞 𝐫𝐮𝐥𝐞𝐫! ⚔️
𝐋𝐞𝐭'𝐬 𝐜𝐨𝐧𝐪𝐮𝐞𝐫! 🏰

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🔥━━━━━━━━━━━━━━━━━━━━━━━🔥
   🐦‍🔥 {user} 🐦‍🔥
   𝐏𝐇𝐎𝐄𝐍𝐈𝐗 𝐑𝐈𝐒𝐄𝐒!
🔥━━━━━━━━━━━━━━━━━━━━━━━🔥

𝐑𝐢𝐬𝐢𝐧𝐠 𝐟𝐫𝐨𝐦 𝐭𝐡𝐞 𝐚𝐬𝐡𝐞𝐬! 🔥
𝐘𝐨𝐮'𝐫𝐞 𝐮𝐧𝐬𝐭𝐨𝐩𝐩𝐚𝐛𝐥𝐞! 💪
𝐁𝐨𝐫𝐧 𝐭𝐨 𝐰𝐢𝐧! 🏆

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🐉━━━━━━━━━━━━━━━━━━━━━━━🐉
   ⚡ {user} ⚡
   𝐃𝐑𝐀𝐆𝐎𝐍 𝐀𝐑𝐑𝐈𝐕𝐄𝐃!
🐉━━━━━━━━━━━━━━━━━━━━━━━🐉

𝐓𝐡𝐞 𝐝𝐫𝐚𝐠𝐨𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞! 🐲
𝐅𝐢𝐫𝐞 𝐢𝐧 𝐭𝐡𝐞 𝐬𝐨𝐮𝐥! 🔥
𝐔𝐧𝐥𝐞𝐚𝐬𝐡 𝐭𝐡𝐞 𝐩𝐨𝐰𝐞𝐫! ⚡

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🐺━━━━━━━━━━━━━━━━━━━━━━━🐺
   🌙 {user} 🌙
   𝐋𝐄𝐆𝐄𝐍𝐃 𝐉𝐎𝐈𝐍𝐒!
🐺━━━━━━━━━━━━━━━━━━━━━━━🐺

𝐓𝐡𝐞 𝐰𝐨𝐥𝐟 𝐡𝐚𝐬 𝐚𝐫𝐫𝐢𝐯𝐞𝐝! 🌕
𝐋𝐞𝐚𝐝𝐞𝐫 𝐨𝐟 𝐭𝐡𝐞 𝐩𝐚𝐜𝐤! 🐾
𝐋𝐞𝐭'𝐬 𝐡𝐨𝐰𝐥! 🌙

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """💪━━━━━━━━━━━━━━━━━━━━━━━💪
   🦍 {user} 🦍
   𝐓𝐈𝐓𝐀𝐍 𝐀𝐑𝐑𝐈𝐕𝐄𝐃!
💪━━━━━━━━━━━━━━━━━━━━━━━💪

𝐀 𝐭𝐢𝐭𝐚𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞! 🏔️
𝐒𝐭𝐫𝐞𝐧𝐠𝐭𝐡 𝐮𝐧𝐥𝐞𝐚𝐬𝐡𝐞𝐝! ⚡
𝐋𝐞𝐭'𝐬 𝐝𝐨𝐦𝐢𝐧𝐚𝐭𝐞! 🔥

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🌌━━━━━━━━━━━━━━━━━━━━━━━🌌
   🚀 {user} 🚀
   𝐆𝐀𝐋𝐀𝐗𝐘 𝐉𝐎𝐈𝐍!
🌌━━━━━━━━━━━━━━━━━━━━━━━🌌

𝐀 𝐬𝐭𝐚𝐫 𝐢𝐬 𝐛𝐨𝐫𝐧! 🌟
𝐁𝐞𝐲𝐨𝐧𝐝 𝐭𝐡𝐢𝐬 𝐰𝐨𝐫𝐥𝐝! 👽
𝐓𝐡𝐞 𝐜𝐨𝐬𝐦𝐨𝐬 𝐰𝐚𝐢𝐭𝐬! 🌠

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🏯━━━━━━━━━━━━━━━━━━━━━━━🏯
   🐯 {user} 🐯
   𝐄𝐌𝐏𝐄𝐑𝐎𝐑 𝐖𝐄𝐋𝐂𝐎𝐌𝐄!
🏯━━━━━━━━━━━━━━━━━━━━━━━🏯

𝐓𝐡𝐞 𝐞𝐦𝐩𝐞𝐫𝐨𝐫 𝐡𝐚𝐬 𝐚𝐫𝐫𝐢𝐯𝐞𝐝! 👑
𝐑𝐞𝐬𝐩𝐞𝐜𝐭 𝐭𝐡𝐞 𝐜𝐫𝐨𝐰𝐧! ⚜️
𝐋𝐞𝐠𝐞𝐧𝐝 𝐛𝐞𝐠𝐢𝐧𝐬! 📜

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🦄━━━━━━━━━━━━━━━━━━━━━━━🦄
   ✨ {user} ✨
   𝐌𝐀𝐆𝐈𝐂 𝐉𝐎𝐈𝐍!
🦄━━━━━━━━━━━━━━━━━━━━━━━🦄

𝐓𝐡𝐞 𝐮𝐧𝐢𝐜𝐨𝐫𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞! 🦄
𝐌𝐚𝐠𝐢𝐜 𝐢𝐧 𝐭𝐡𝐞 𝐚𝐢𝐫! ✨
𝐘𝐨𝐮'𝐫𝐞 𝐨𝐧𝐞 𝐨𝐟 𝐚 𝐤𝐢𝐧𝐝! 💫

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🦈━━━━━━━━━━━━━━━━━━━━━━━🦈
   ⚓ {user} ⚓
   𝐄𝐋𝐈𝐓𝐄 𝐀𝐑𝐑𝐈𝐕𝐄𝐃!
🦈━━━━━━━━━━━━━━━━━━━━━━━🦈

𝐓𝐡𝐞 𝐬𝐡𝐚𝐫𝐤 𝐢𝐬 𝐡𝐞𝐫𝐞! 🌊
𝐑𝐮𝐥𝐞 𝐭𝐡𝐞 𝐝𝐞𝐞𝐩! 🏊
𝐔𝐧𝐬𝐭𝐨𝐩𝐩𝐚𝐛𝐥𝐞 𝐟𝐨𝐫𝐜𝐞! 💪

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🦅━━━━━━━━━━━━━━━━━━━━━━━🦅
   ☀️ {user} ☀️
   𝐑𝐎𝐘𝐀𝐋 𝐅𝐋𝐘!
🦅━━━━━━━━━━━━━━━━━━━━━━━🦅

𝐓𝐡𝐞 𝐞𝐚𝐠𝐥𝐞 𝐡𝐚𝐬 𝐟𝐥𝐨𝐰𝐧! 🦅
𝐅𝐥𝐲 𝐡𝐢𝐠𝐡! 𝐃𝐫𝐞𝐚𝐦 𝐛𝐢𝐠! ☀️
𝐓𝐡𝐞 𝐬𝐤𝐲 𝐢𝐬 𝐭𝐡𝐞 𝐥𝐢𝐦𝐢𝐭! 🌤️

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━"""
]

# ---------- BAN MESSAGES (10) ----------
BAN_MESSAGES = [
    """⚖️━━━━━━━━━━━━━━━━━━━━━━━⚖️
   ⛔️ {user} ⛔️
   𝐉𝐔𝐒𝐓𝐈𝐂𝐄 𝐒𝐄𝐑𝐕𝐄𝐃!
⚖️━━━━━━━━━━━━━━━━━━━━━━━⚖️

𝐑𝐮𝐥𝐞𝐬 𝐰𝐞𝐫𝐞 𝐛𝐫𝐨𝐤𝐞𝐧! 🚨
𝐀𝐜𝐭𝐢𝐨𝐧 𝐰𝐚𝐬 𝐧𝐞𝐞𝐝𝐞𝐝! ⚡
𝐓𝐡𝐞 𝐠𝐫𝐨𝐮𝐩 𝐢𝐬 𝐬𝐚𝐟𝐞! 🛡️

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🔨━━━━━━━━━━━━━━━━━━━━━━━🔨
   🚷 {user} 🚷
   𝐁𝐀𝐍 𝐇𝐀𝐌𝐌𝐄𝐑!
🔨━━━━━━━━━━━━━━━━━━━━━━━🔨

𝐎𝐮𝐭 𝐨𝐟 𝐭𝐡𝐞 𝐠𝐚𝐦𝐞! ⚽
𝐍𝐨 𝐭𝐨𝐥𝐞𝐫𝐚𝐧𝐜𝐞! ❌
𝐑𝐮𝐥𝐞𝐬 𝐚𝐫𝐞 𝐫𝐮𝐥𝐞𝐬! 📜

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🚀━━━━━━━━━━━━━━━━━━━━━━━🚀
   💢 {user} 💢
   𝐄𝐉𝐄𝐂𝐓𝐄𝐃!
🚀━━━━━━━━━━━━━━━━━━━━━━━🚀

𝐘𝐨𝐮'𝐫𝐞 𝐨𝐮𝐭! 🌌
𝐓𝐡𝐞 𝐠𝐫𝐨𝐮𝐩 𝐦𝐨𝐯𝐞𝐬 𝐨𝐧! 🚶
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🔒━━━━━━━━━━━━━━━━━━━━━━━🔒
   🚷 {user} 🚷
   𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 𝐋𝐎𝐂𝐊!
🔒━━━━━━━━━━━━━━━━━━━━━━━🔒

𝐀𝐜𝐜𝐞𝐬𝐬 𝐝𝐞𝐧𝐢𝐞𝐝! 🚫
𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝! 🛡️
𝐒𝐚𝐟𝐞 𝐬𝐩𝐚𝐜𝐞 𝐦𝐚𝐢𝐧𝐭𝐚𝐢𝐧𝐞𝐝! ✨

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🚫━━━━━━━━━━━━━━━━━━━━━━━🚫
   ⛔️ {user} ⛔️
   𝐎𝐔𝐓𝐂𝐀𝐒𝐓!
🚫━━━━━━━━━━━━━━━━━━━━━━━🚫

𝐍𝐨 𝐦𝐨𝐫𝐞 𝐜𝐡𝐚𝐧𝐜𝐞𝐬! ❌
𝐖𝐚𝐫𝐧𝐢𝐧𝐠𝐬 𝐰𝐞𝐫𝐞 𝐢𝐠𝐧𝐨𝐫𝐞𝐝! 👀
𝐓𝐢𝐦𝐞 𝐭𝐨 𝐠𝐨! 🚪

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """💀━━━━━━━━━━━━━━━━━━━━━━━💀
   ⚡ {user} ⚡
   𝐓𝐄𝐑𝐌𝐈𝐍𝐀𝐓𝐄𝐃!
💀━━━━━━━━━━━━━━━━━━━━━━━💀

𝐆𝐚𝐦𝐞 𝐨𝐯𝐞𝐫! 🎮
𝐍𝐨 𝐫𝐞𝐭𝐮𝐫𝐧! 🚫
𝐓𝐡𝐞 𝐞𝐧𝐝! 💥

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🗡️━━━━━━━━━━━━━━━━━━━━━━━🗡️
   💢 {user} 💢
   𝐁𝐀𝐍𝐈𝐒𝐇𝐄𝐃!
🗡️━━━━━━━━━━━━━━━━━━━━━━━🗡️

𝐅𝐨𝐫𝐞𝐯𝐞𝐫 𝐠𝐨𝐧𝐞! 🌅
𝐑𝐮𝐥𝐞𝐬 𝐰𝐞𝐫𝐞 𝐜𝐥𝐞𝐚𝐫! 📋
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🔐━━━━━━━━━━━━━━━━━━━━━━━🔐
   🚷 {user} 🚷
   𝐁𝐋𝐎𝐂𝐊𝐄𝐃!
🔐━━━━━━━━━━━━━━━━━━━━━━━🔐

𝐍𝐨 𝐞𝐧𝐭𝐫𝐲! 🚪
𝐏𝐞𝐫𝐦𝐚𝐧𝐞𝐧𝐭 𝐚𝐜𝐭𝐢𝐨𝐧! ⚖️
𝐌𝐨𝐯𝐞 𝐨𝐧! 🚶

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🎯━━━━━━━━━━━━━━━━━━━━━━━🎯
   ⛔️ {user} ⛔️
   𝐄𝐗𝐏𝐄𝐋𝐋𝐄𝐃!
🎯━━━━━━━━━━━━━━━━━━━━━━━🎯

𝐓𝐚𝐫𝐠𝐞𝐭 𝐫𝐞𝐦𝐨𝐯𝐞𝐝! 🎯
𝐍𝐨 𝐦𝐞𝐫𝐜𝐲! ❌
𝐓𝐡𝐞 𝐫𝐮𝐥𝐞𝐬 𝐰𝐢𝐧! ⚔️

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """💥━━━━━━━━━━━━━━━━━━━━━━━💥
   💢 {user} 💢
   𝐔𝐋𝐓𝐈𝐌𝐀𝐓𝐄 𝐁𝐀𝐍!
💥━━━━━━━━━━━━━━━━━━━━━━━💥

𝐅𝐢𝐧𝐚𝐥 𝐬𝐭𝐫𝐢𝐤𝐞! ⚡
𝐍𝐨 𝐜𝐨𝐦𝐢𝐧𝐠 𝐛𝐚𝐜𝐤! 🚫
𝐈𝐭'𝐬 𝐨𝐯𝐞𝐫! 🎬

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━"""
]

# ---------- LEFT MESSAGES (10) ----------
LEFT_MESSAGES = [
    """👋━━━━━━━━━━━━━━━━━━━━━━━👋
   💔 {user} 💔
   𝐆𝐎𝐎𝐃𝐁𝐘𝐄!
👋━━━━━━━━━━━━━━━━━━━━━━━👋

𝐖𝐞'𝐥𝐥 𝐦𝐢𝐬𝐬 𝐲𝐨𝐮! 🥺
𝐓𝐚𝐤𝐞 𝐜𝐚𝐫𝐞! 🌈
𝐇𝐨𝐩𝐞 𝐭𝐨 𝐬𝐞𝐞 𝐲𝐨𝐮 𝐚𝐠𝐚𝐢𝐧! 🌟

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🚶━━━━━━━━━━━━━━━━━━━━━━━🚶
   🌅 {user} 🌅
   𝐃𝐄𝐏𝐀𝐑𝐓𝐔𝐑𝐄!
🚶━━━━━━━━━━━━━━━━━━━━━━━🚶

𝐖𝐚𝐥𝐤𝐢𝐧𝐠 𝐚𝐰𝐚𝐲! 🚶
𝐓𝐡𝐞 𝐬𝐮𝐧 𝐬𝐞𝐭𝐬! 🌅
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🕊️━━━━━━━━━━━━━━━━━━━━━━━🕊️
   💫 {user} 💫
   𝐋𝐎𝐒𝐓 𝐒𝐎𝐔𝐋!
🕊️━━━━━━━━━━━━━━━━━━━━━━━🕊️

𝐅𝐥𝐲 𝐡𝐢𝐠𝐡! 🕊️
𝐅𝐢𝐧𝐝 𝐲𝐨𝐮𝐫 𝐰𝐚𝐲! 🌟
𝐘𝐨𝐮'𝐥𝐥 𝐛𝐞 𝐦𝐢𝐬𝐬𝐞𝐝! 💔

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🌊━━━━━━━━━━━━━━━━━━━━━━━🌊
   🚣 {user} 🚣
   𝐌𝐎𝐕𝐈𝐍𝐆 𝐎𝐍!
🌊━━━━━━━━━━━━━━━━━━━━━━━🌊

𝐒𝐚𝐢𝐥𝐢𝐧𝐠 𝐚𝐰𝐚𝐲! ⛵
𝐅𝐢𝐧𝐝 𝐩𝐞𝐚𝐜𝐞! 🌅
𝐓𝐡𝐞 𝐬𝐞𝐚 𝐰𝐚𝐢𝐭𝐬! 🌊

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """✌️━━━━━━━━━━━━━━━━━━━━━━━✌️
   ☮️ {user} ☮️
   𝐏𝐄𝐀𝐂𝐄 𝐎𝐔𝐓!
✌️━━━━━━━━━━━━━━━━━━━━━━━✌️

𝐒𝐩𝐫𝐞𝐚𝐝 𝐥𝐨𝐯𝐞! ❤️
𝐅𝐢𝐧𝐝 𝐣𝐨𝐲! 😊
𝐓𝐚𝐤𝐞 𝐜𝐚𝐫𝐞! ✌️

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🌹━━━━━━━━━━━━━━━━━━━━━━━🌹
   🥀 {user} 🥀
   𝐅𝐀𝐑𝐄𝐖𝐄𝐋𝐋!
🌹━━━━━━━━━━━━━━━━━━━━━━━🌹

𝐀 𝐫𝐨𝐬𝐞 𝐡𝐚𝐬 𝐟𝐚𝐥𝐥𝐞𝐧! 🌹
𝐁𝐮𝐭 𝐥𝐞𝐠𝐞𝐧𝐝𝐬 𝐫𝐞𝐦𝐚𝐢𝐧! 📜
𝐒𝐞𝐞 𝐲𝐨𝐮 𝐬𝐨𝐨𝐧! 👋

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🌙━━━━━━━━━━━━━━━━━━━━━━━🌙
   🌟 {user} 🌟
   𝐌𝐎𝐎𝐍𝐋𝐈𝐆𝐇𝐓!
🌙━━━━━━━━━━━━━━━━━━━━━━━🌙

𝐓𝐡𝐞 𝐦𝐨𝐨𝐧 𝐫𝐢𝐬𝐞𝐬! 🌙
𝐓𝐡𝐞 𝐬𝐭𝐚𝐫 𝐟𝐚𝐥𝐥𝐬! 🌟
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 🌌

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """♾️━━━━━━━━━━━━━━━━━━━━━━━♾️
   🌈 {user} 🌈
   𝐄𝐍𝐃𝐋𝐄𝐒𝐒!
♾️━━━━━━━━━━━━━━━━━━━━━━━♾️

𝐓𝐡𝐞 𝐣𝐨𝐮𝐫𝐧𝐞𝐲 𝐞𝐧𝐝𝐬! 🚶
𝐁𝐮𝐭 𝐦𝐞𝐦𝐨𝐫𝐢𝐞𝐬 𝐥𝐚𝐬𝐭! 💫
𝐅𝐢𝐧𝐝 𝐲𝐨𝐮𝐫 𝐫𝐚𝐢𝐧𝐛𝐨𝐰! 🌈

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🦋━━━━━━━━━━━━━━━━━━━━━━━🦋
   🌺 {user} 🌺
   𝐁𝐔𝐓𝐓𝐄𝐑𝐅𝐋𝐘!
🦋━━━━━━━━━━━━━━━━━━━━━━━🦋

𝐒𝐩𝐫𝐞𝐚𝐝 𝐲𝐨𝐮𝐫 𝐰𝐢𝐧𝐠𝐬! 🦋
𝐅𝐥𝐲 𝐟𝐫𝐞𝐞! 🌸
𝐅𝐢𝐧𝐝 𝐧𝐞𝐰 𝐠𝐚𝐫𝐝𝐞𝐧𝐬! 🌻

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """✨━━━━━━━━━━━━━━━━━━━━━━━✨
   ☄️ {user} ☄️
   𝐒𝐓𝐀𝐑𝐃𝐔𝐒𝐓!
✨━━━━━━━━━━━━━━━━━━━━━━━✨

𝐀 𝐬𝐭𝐚𝐫 𝐡𝐚𝐬 𝐠𝐨𝐧𝐞! 🌟
𝐁𝐮𝐭 𝐬𝐡𝐢𝐧𝐞𝐬 𝐞𝐥𝐬𝐞𝐰𝐡𝐞𝐫𝐞! ✨
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
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
        
        emojis = ["🔥", "✨", "💎", "🌟", "🎉", "🚀", "👑", "💫", "⭐️", "🌈"]
        footer = random.sample(emojis, 4)
        msg_text += f"\n\n{footer[0]} **ᴘʀᴇᴍɪᴜᴍ** {footer[1]} **ᴜᴘᴅᴀᴛᴇ** {footer[2]} **ʙʏ** {footer[3]} **ʙᴏᴛ**"
        
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

# ========== GROUP AUTO-ADD HANDLER ==========
@app.on_message(filters.group & filters.command("addgroup") & filters.user(OWNER_ID))
async def add_group_from_group(client, message: Message):
    try:
        chat_id = message.chat.id
        chat_name = message.chat.title or f"Group {chat_id}"
        
        save_group(chat_id, chat_name)
        
        confirm_text = f"""✅━━━━━━━━━━━━━━━━━━━━━━━✅
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃   🎯 𝗚𝗥𝗢𝗨𝗣 𝗔𝗗𝗗𝗘𝗗  🎯
┗━━━━━━━━━━━━━━━━━━━━━━━┛
✅━━━━━━━━━━━━━━━━━━━━━━━✅

📛 **𝗡𝗔𝗠𝗘:** `{chat_name}`
🆔 **𝗜𝗗:** `{chat_id}`
📅 **𝗗𝗔𝗧𝗘:** `{get_current_date()}`
🕐 **𝗧𝗜𝗠𝗘:** `{get_current_time()}`

━━━━━━━━━━━━━━━━━━━━━━━
🌟 **𝗦𝗧𝗔𝗧𝗨𝗦:** ✅ 𝗔𝗖𝗧𝗜𝗩𝗘
━━━━━━━━━━━━━━━━━━━━━━━

⚡️ **𝗡𝗢𝗪 𝗠𝗢𝗡𝗜𝗧𝗢𝗥𝗜𝗡𝗚:**
• 👤 𝗝𝗼𝗶𝗻𝘀
• 🚶 𝗟𝗲𝗮𝘃𝗲𝘀  
• 🚫 𝗕𝗮𝗻𝘀

━━━━━━━━━━━━━━━━━━━━━━━
🌌 **𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗘𝗡𝗔𝗕𝗟𝗘𝗗** 🌌
━━━━━━━━━━━━━━━━━━━━━━━"""

        sent_msg = await message.reply_text(confirm_text)
        
        await asyncio.sleep(5)
        try:
            await sent_msg.delete()
            await message.delete()
        except:
            pass
        
        logger.info(f"✅ Group auto-added: {chat_name} ({chat_id})")
        
    except Exception as e:
        await message.reply_text(f"❌ **ᴇʀʀᴏʀ:** {str(e)}")
        logger.error(f"❌ Error in group add: {e}")

# ========== SERVICE MESSAGES HANDLER ==========
@app.on_message(filters.group & filters.service)
async def service_message_handler(client, message: Message):
    try:
        chat_id = message.chat.id
        
        if not is_group_enabled(chat_id):
            return
        
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
        
        elif message.left_chat_member:
            user = message.left_chat_member
            if user.is_bot:
                return
                
            mention = f"[{user.first_name}](tg://user?id={user.id})"
            
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

# ========== START COMMAND ==========
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    if not is_owner(message.from_user.id):
        await message.reply_text("❌ **ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇss!**")
        return
    
    videos = get_video_count()
    groups = len(get_all_groups())
    
    await message.reply_text(
        f"""🌌━━━━━━━━━━━━━━━━━━━━━━━🌌
┏━━━━━━━━━━━━━━━━━━━━━━━┓
┃    🌌 ᴘʀᴇᴍɪᴜᴍ ʙᴏᴛ 🌌     
┗━━━━━━━━━━━━━━━━━━━━━━━┛
🌌━━━━━━━━━━━━━━━━━━━━━━━🌌

ʜᴇʏ **{message.from_user.first_name}**! 🚀  
ʙᴏᴛ ɪs ʀᴜɴɴɪɴɢ sᴍᴏᴏᴛʜʟʏ ✨

━━━━━━━━━━━━━━━━━━━━━━━
📹 **ᴠɪᴅᴇᴏs:** `{videos}`  │  👥 **ɢʀᴏᴜᴘs:** `{groups}`
━━━━━━━━━━━━━━━━━━━━━━━

📹 `/addvideo` - ᴀᴅᴅ ᴠɪᴅᴇᴏ  
📋 `/videos` - ᴠɪᴇᴡ ᴀʟʟ  
🗑️ `/delvideo` - ᴅᴇʟᴇᴛᴇ  
🧹 `/clearvideos` - ᴄʟᴇᴀʀ ᴀʟʟ  

➕ `/addgroup` - ᴀᴅᴅ ɢʀᴏᴜᴘ  
📋 `/groups` - ᴠɪᴇᴡ ᴀʟʟ  
❌ `/delgroup` - ʀᴇᴍᴏᴠᴇ  
🔄 `/toggle` - ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ  

📊 `/stats` - ʙᴏᴛ sᴛᴀᴛs  

━━━━━━━━━━━━━━━━━━━━━━━
🌌 **ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴇ** 🌌
━━━━━━━━━━━━━━━━━━━━━━━"""
    )

# ========== ADD GROUP PRIVATE ==========
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

# ========== GROUPS LIST ==========
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

# ========== DELETE GROUP ==========
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

# ========== TOGGLE GROUP ==========
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

# ========== ADD VIDEO ==========
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

# ========== VIDEOS LIST ==========
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

# ========== DELETE VIDEO ==========
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

# ========== CLEAR VIDEOS ==========
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

# ========== STATS ==========
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
🌌 **ᴘʀᴇᴍɪᴜᴍ** ʙᴏᴛ 🌌
━━━━━━━━━━━━━━━━━━━━━━━"""
    
    await message.reply_text(text)

# ========== RUN ==========
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 STARTING PREMIUM BOT...")
    print("🌌 GALACTIC THEME ACTIVE")
    print("="*60 + "\n")
    
    if not os.path.exists(VIDEO_DB):
        with open(VIDEO_DB, "w") as f:
            json.dump([], f)
    
    if not os.path.exists(GROUPS_DB):
        with open(GROUPS_DB, "w") as f:
            json.dump({}, f)
    
    os.makedirs("downloads", exist_ok=True)
    
    print(f"📹 Total videos: {get_video_count()}")
    print(f"👥 Total groups: {len(get_all_groups())}")
    print("\n" + "="*60)
    print("🤖 BOT IS RUNNING!")
    print("🌌 HAR BAAR NAYI VIDEO AAYEGI!")
    print("="*60 + "\n")
    
    try:
        app.run()
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
