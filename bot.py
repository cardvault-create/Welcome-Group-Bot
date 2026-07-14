import asyncio
import json
import random
import os
import logging
from datetime import datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# ========== LOGGING ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== 🔴 APNA DATA DAALO ==========
API_ID = 35140329
API_HASH = "011f638e4acadee178c59afffc80193d"
BOT_TOKEN = "8603632286:AAE8Hw5xWzKjrpr4r7PrrMifZxu7-v93TaM"
OWNER_ID = 7614459746
OWNER_USERNAME = "BESTCHEAT_OWNER"

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

# ========== JOIN MESSAGES ==========
JOIN_MESSAGES = [
    """🔥━━━━━━━━━━━━━━━━━━━━━🔥
   🐦‍🔥 {user} 🐦‍🔥
   𝐏𝐇𝐎𝐄𝐍𝐈𝐗 𝐑𝐈𝐒𝐄𝐒!
🔥━━━━━━━━━━━━━━━━━━━━━🔥

𝐑𝐢𝐬𝐢𝐧𝐠 𝐟𝐫𝐨𝐦 𝐭𝐡𝐞 𝐚𝐬𝐡𝐞𝐬! 🔥
𝐘𝐨𝐮'𝐫𝐞 𝐮𝐧𝐬𝐭𝐨𝐩𝐩𝐚𝐛𝐥𝐞! 💪
𝐁𝐨𝐫𝐧 𝐭𝐨 𝐰𝐢𝐧! 🏆

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """👑━━━━━━━━━━━━━━━━━━━━━👑
   🦁 {user} 🦁
   𝐊𝐈𝐍𝐆 𝐖𝐄𝐋𝐂𝐎𝐌𝐄!
👑━━━━━━━━━━━━━━━━━━━━━👑

𝐓𝐡𝐞 𝐤𝐢𝐧𝐠 𝐢𝐬 𝐡𝐞𝐫𝐞! 👑
𝐘𝐨𝐮'𝐫𝐞 𝐭𝐡𝐞 𝐫𝐮𝐥𝐞𝐫! ⚔️
𝐋𝐞𝐭'𝐬 𝐜𝐨𝐧𝐪𝐮𝐞𝐫! 🏰

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🐉━━━━━━━━━━━━━━━━━━━━━🐉
   ⚡ {user} ⚡
   𝐃𝐑𝐀𝐆𝐎𝐍 𝐀𝐑𝐑𝐈𝐕𝐄𝐃!
🐉━━━━━━━━━━━━━━━━━━━━━🐉

𝐓𝐡𝐞 𝐝𝐫𝐚𝐠𝐨𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞! 🐲
𝐅𝐢𝐫𝐞 𝐢𝐧 𝐭𝐡𝐞 𝐬𝐨𝐮𝐥! 🔥
𝐔𝐧𝐥𝐞𝐚𝐬𝐡 𝐭𝐡𝐞 𝐩𝐨𝐰𝐞𝐫! ⚡

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🐺━━━━━━━━━━━━━━━━━━━━━🐺
   🌙 {user} 🌙
   𝐋𝐄𝐆𝐄𝐍𝐃 𝐉𝐎𝐈𝐍𝐒!
🐺━━━━━━━━━━━━━━━━━━━━━🐺

𝐓𝐡𝐞 𝐰𝐨𝐥𝐟 𝐡𝐚𝐬 𝐚𝐫𝐫𝐢𝐯𝐞𝐝! 🌕
𝐋𝐞𝐚𝐝𝐞𝐫 𝐨𝐟 𝐭𝐡𝐞 𝐩𝐚𝐜𝐤! 🐾
𝐋𝐞𝐭'𝐬 𝐡𝐨𝐰𝐥! 🌙

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """💪━━━━━━━━━━━━━━━━━━━━━💪
   🦍 {user} 🦍
   𝐓𝐈𝐓𝐀𝐍 𝐀𝐑𝐑𝐈𝐕𝐄𝐃!
💪━━━━━━━━━━━━━━━━━━━━━💪

𝐀 𝐭𝐢𝐭𝐚𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞! 🏔️
𝐒𝐭𝐫𝐞𝐧𝐠𝐭𝐡 𝐮𝐧𝐥𝐞𝐚𝐬𝐡𝐞𝐝! ⚡
𝐋𝐞𝐭'𝐬 𝐝𝐨𝐦𝐢𝐧𝐚𝐭𝐞! 🔥

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🌌━━━━━━━━━━━━━━━━━━━━━🌌
   🚀 {user} 🚀
   𝐆𝐀𝐋𝐀𝐗𝐘 𝐉𝐎𝐈𝐍!
🌌━━━━━━━━━━━━━━━━━━━━━🌌

𝐀 𝐬𝐭𝐚𝐫 𝐢𝐬 𝐛𝐨𝐫𝐧! 🌟
𝐁𝐞𝐲𝐨𝐧𝐝 𝐭𝐡𝐢𝐬 𝐰𝐨𝐫𝐥𝐝! 👽
𝐓𝐡𝐞 𝐜𝐨𝐬𝐦𝐨𝐬 𝐰𝐚𝐢𝐭𝐬! 🌠

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🏯━━━━━━━━━━━━━━━━━━━━━🏯
   🐯 {user} 🐯
   𝐄𝐌𝐏𝐄𝐑𝐎𝐑 𝐖𝐄𝐋𝐂𝐎𝐌𝐄!
🏯━━━━━━━━━━━━━━━━━━━━━🏯

𝐓𝐡𝐞 𝐞𝐦𝐩𝐞𝐫𝐨𝐫 𝐡𝐚𝐬 𝐚𝐫𝐫𝐢𝐯𝐞𝐝! 👑
𝐑𝐞𝐬𝐩𝐞𝐜𝐭 𝐭𝐡𝐞 𝐜𝐫𝐨𝐰𝐧! ⚜️
𝐋𝐞𝐠𝐞𝐧𝐝 𝐛𝐞𝐠𝐢𝐧𝐬! 📜

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🦄━━━━━━━━━━━━━━━━━━━━━🦄
   ✨ {user} ✨
   𝐌𝐀𝐆𝐈𝐂 𝐉𝐎𝐈𝐍!
🦄━━━━━━━━━━━━━━━━━━━━━🦄

𝐓𝐡𝐞 𝐮𝐧𝐢𝐜𝐨𝐫𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞! 🦄
𝐌𝐚𝐠𝐢𝐜 𝐢𝐧 𝐭𝐡𝐞 𝐚𝐢𝐫! ✨
𝐘𝐨𝐮'𝐫𝐞 𝐨𝐧𝐞 𝐨𝐟 𝐚 𝐤𝐢𝐧𝐝! 💫

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🦈━━━━━━━━━━━━━━━━━━━━━🦈
   ⚓ {user} ⚓
   𝐄𝐋𝐈𝐓𝐄 𝐀𝐑𝐑𝐈𝐕𝐄𝐃!
🦈━━━━━━━━━━━━━━━━━━━━━🦈

𝐓𝐡𝐞 𝐬𝐡𝐚𝐫𝐤 𝐢𝐬 𝐡𝐞𝐫𝐞! 🌊
𝐑𝐮𝐥𝐞 𝐭𝐡𝐞 𝐝𝐞𝐞𝐩! 🏊
𝐔𝐧𝐬𝐭𝐨𝐩𝐩𝐚𝐛𝐥𝐞 𝐟𝐨𝐫𝐜𝐞! 💪

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🦅━━━━━━━━━━━━━━━━━━━━━🦅
   ☀️ {user} ☀️
   𝐑𝐎𝐘𝐀𝐋 𝐅𝐋𝐘!
🦅━━━━━━━━━━━━━━━━━━━━━🦅

𝐓𝐡𝐞 𝐞𝐚𝐠𝐥𝐞 𝐡𝐚𝐬 𝐟𝐥𝐨𝐰𝐧! 🦅
𝐅𝐥𝐲 𝐡𝐢𝐠𝐡! 𝐃𝐫𝐞𝐚𝐦 𝐛𝐢𝐠! ☀️
𝐓𝐡𝐞 𝐬𝐤𝐲 𝐢𝐬 𝐭𝐡𝐞 𝐥𝐢𝐦𝐢𝐭! 🌤️

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━"""
]

# ========== BAN MESSAGES ==========
BAN_MESSAGES = [
    """⚖️━━━━━━━━━━━━━━━━━━━━━⚖️
   ⛔️ {user} ⛔️
   𝐉𝐔𝐒𝐓𝐈𝐂𝐄 𝐒𝐄𝐑𝐕𝐄𝐃!
⚖️━━━━━━━━━━━━━━━━━━━━━⚖️

𝐑𝐮𝐥𝐞𝐬 𝐰𝐞𝐫𝐞 𝐛𝐫𝐨𝐤𝐞𝐧! 🚨
𝐀𝐜𝐭𝐢𝐨𝐧 𝐰𝐚𝐬 𝐧𝐞𝐞𝐝𝐞𝐝! ⚡
𝐓𝐡𝐞 𝐠𝐫𝐨𝐮𝐩 𝐢𝐬 𝐬𝐚𝐟𝐞! 🛡️

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🔨━━━━━━━━━━━━━━━━━━━━━🔨
   🚷 {user} 🚷
   𝐁𝐀𝐍 𝐇𝐀𝐌𝐌𝐄𝐑!
🔨━━━━━━━━━━━━━━━━━━━━━🔨

𝐎𝐮𝐭 𝐨𝐟 𝐭𝐡𝐞 𝐠𝐚𝐦𝐞! ⚽
𝐍𝐨 𝐭𝐨𝐥𝐞𝐫𝐚𝐧𝐜𝐞! ❌
𝐑𝐮𝐥𝐞𝐬 𝐚𝐫𝐞 𝐫𝐮𝐥𝐞𝐬! 📜

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🚀━━━━━━━━━━━━━━━━━━━━━🚀
   💢 {user} 💢
   𝐄𝐉𝐄𝐂𝐓𝐄𝐃!
🚀━━━━━━━━━━━━━━━━━━━━━🚀

𝐘𝐨𝐮'𝐫𝐞 𝐨𝐮𝐭! 🌌
𝐓𝐡𝐞 𝐠𝐫𝐨𝐮𝐩 𝐦𝐨𝐯𝐞𝐬 𝐨𝐧! 🚶
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🔒━━━━━━━━━━━━━━━━━━━━━🔒
   🚷 {user} 🚷
   𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 𝐋𝐎𝐂𝐊!
🔒━━━━━━━━━━━━━━━━━━━━━🔒

𝐀𝐜𝐜𝐞𝐬𝐬 𝐝𝐞𝐧𝐢𝐞𝐝! 🚫
𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝! 🛡️
𝐒𝐚𝐟𝐞 𝐬𝐩𝐚𝐜𝐞 𝐦𝐚𝐢𝐧𝐭𝐚𝐢𝐧𝐞𝐝! ✨

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🚫━━━━━━━━━━━━━━━━━━━━━🚫
   ⛔️ {user} ⛔️
   𝐎𝐔𝐓𝐂𝐀𝐒𝐓!
🚫━━━━━━━━━━━━━━━━━━━━━🚫

𝐍𝐨 𝐦𝐨𝐫𝐞 𝐜𝐡𝐚𝐧𝐜𝐞𝐬! ❌
𝐖𝐚𝐫𝐧𝐢𝐧𝐠𝐬 𝐰𝐞𝐫𝐞 𝐢𝐠𝐧𝐨𝐫𝐞𝐝! 👀
𝐓𝐢𝐦𝐞 𝐭𝐨 𝐠𝐨! 🚪

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """💀━━━━━━━━━━━━━━━━━━━━━💀
   ⚡ {user} ⚡
   𝐓𝐄𝐑𝐌𝐈𝐍𝐀𝐓𝐄𝐃!
💀━━━━━━━━━━━━━━━━━━━━━💀

𝐆𝐚𝐦𝐞 𝐨𝐯𝐞𝐫! 🎮
𝐍𝐨 𝐫𝐞𝐭𝐮𝐫𝐧! 🚫
𝐓𝐡𝐞 𝐞𝐧𝐝! 💥

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🗡️━━━━━━━━━━━━━━━━━━━━━🗡️
   💢 {user} 💢
   𝐁𝐀𝐍𝐈𝐒𝐇𝐄𝐃!
🗡️━━━━━━━━━━━━━━━━━━━━━🗡️

𝐅𝐨𝐫𝐞𝐯𝐞𝐫 𝐠𝐨𝐧𝐞! 🌅
𝐑𝐮𝐥𝐞𝐬 𝐰𝐞𝐫𝐞 𝐜𝐥𝐞𝐚𝐫! 📋
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🔐━━━━━━━━━━━━━━━━━━━━━🔐
   🚷 {user} 🚷
   𝐁𝐋𝐎𝐂𝐊𝐄𝐃!
🔐━━━━━━━━━━━━━━━━━━━━━🔐

𝐍𝐨 𝐞𝐧𝐭𝐫𝐲! 🚪
𝐏𝐞𝐫𝐦𝐚𝐧𝐞𝐧𝐭 𝐚𝐜𝐭𝐢𝐨𝐧! ⚖️
𝐌𝐨𝐯𝐞 𝐨𝐧! 🚶

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🎯━━━━━━━━━━━━━━━━━━━━━🎯
   ⛔️ {user} ⛔️
   𝐄𝐗𝐏𝐄𝐋𝐋𝐄𝐃!
🎯━━━━━━━━━━━━━━━━━━━━━🎯

𝐓𝐚𝐫𝐠𝐞𝐭 𝐫𝐞𝐦𝐨𝐯𝐞𝐝! 🎯
𝐍𝐨 𝐦𝐞𝐫𝐜𝐲! ❌
𝐓𝐡𝐞 𝐫𝐮𝐥𝐞𝐬 𝐰𝐢𝐧! ⚔️

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """💥━━━━━━━━━━━━━━━━━━━━━💥
   💢 {user} 💢
   𝐔𝐋𝐓𝐈𝐌𝐀𝐓𝐄 𝐁𝐀𝐍!
💥━━━━━━━━━━━━━━━━━━━━━💥

𝐅𝐢𝐧𝐚𝐥 𝐬𝐭𝐫𝐢𝐤𝐞! ⚡
𝐍𝐨 𝐜𝐨𝐦𝐢𝐧𝐠 𝐛𝐚𝐜𝐤! 🚫
𝐈𝐭'𝐬 𝐨𝐯𝐞𝐫! 🎬

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━"""
]

# ========== LEFT MESSAGES ==========
LEFT_MESSAGES = [
    """👋━━━━━━━━━━━━━━━━━━━━━👋
   💔 {user} 💔
   𝐆𝐎𝐎𝐃𝐁𝐘𝐄!
👋━━━━━━━━━━━━━━━━━━━━━👋

𝐖𝐞'𝐥𝐥 𝐦𝐢𝐬𝐬 𝐲𝐨𝐮! 🥺
𝐓𝐚𝐤𝐞 𝐜𝐚𝐫𝐞! 🌈
𝐇𝐨𝐩𝐞 𝐭𝐨 𝐬𝐞𝐞 𝐲𝐨𝐮 𝐚𝐠𝐚𝐢𝐧! 🌟

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🚶━━━━━━━━━━━━━━━━━━━━━🚶
   🌅 {user} 🌅
   𝐃𝐄𝐏𝐀𝐑𝐓𝐔𝐑𝐄!
🚶━━━━━━━━━━━━━━━━━━━━━🚶

𝐖𝐚𝐥𝐤𝐢𝐧𝐠 𝐚𝐰𝐚𝐲! 🚶
𝐓𝐡𝐞 𝐬𝐮𝐧 𝐬𝐞𝐭𝐬! 🌅
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🕊️━━━━━━━━━━━━━━━━━━━━━🕊️
   💫 {user} 💫
   𝐋𝐎𝐒𝐓 𝐒𝐎𝐔𝐋!
🕊️━━━━━━━━━━━━━━━━━━━━━🕊️

𝐅𝐥𝐲 𝐡𝐢𝐠𝐡! 🕊️
𝐅𝐢𝐧𝐝 𝐲𝐨𝐮𝐫 𝐰𝐚𝐲! 🌟
𝐘𝐨𝐮'𝐥𝐥 𝐛𝐞 𝐦𝐢𝐬𝐬𝐞𝐝! 💔

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🌊━━━━━━━━━━━━━━━━━━━━━🌊
   🚣 {user} 🚣
   𝐌𝐎𝐕𝐈𝐍𝐆 𝐎𝐍!
🌊━━━━━━━━━━━━━━━━━━━━━🌊

𝐒𝐚𝐢𝐥𝐢𝐧𝐠 𝐚𝐰𝐚𝐲! ⛵
𝐅𝐢𝐧𝐝 𝐩𝐞𝐚𝐜𝐞! 🌅
𝐓𝐡𝐞 𝐬𝐞𝐚 𝐰𝐚𝐢𝐭𝐬! 🌊

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """✌️━━━━━━━━━━━━━━━━━━━━━✌️
   ☮️ {user} ☮️
   𝐏𝐄𝐀𝐂𝐄 𝐎𝐔𝐓!
✌️━━━━━━━━━━━━━━━━━━━━━✌️

𝐒𝐩𝐫𝐞𝐚𝐝 𝐥𝐨𝐯𝐞! ❤️
𝐅𝐢𝐧𝐝 𝐣𝐨𝐲! 😊
𝐓𝐚𝐤𝐞 𝐜𝐚𝐫𝐞! ✌️

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🌹━━━━━━━━━━━━━━━━━━━━━🌹
   🥀 {user} 🥀
   𝐅𝐀𝐑𝐄𝐖𝐄𝐋𝐋!
🌹━━━━━━━━━━━━━━━━━━━━━🌹

𝐀 𝐫𝐨𝐬𝐞 𝐡𝐚𝐬 𝐟𝐚𝐥𝐥𝐞𝐧! 🌹
𝐁𝐮𝐭 𝐥𝐞𝐠𝐞𝐧𝐝𝐬 𝐫𝐞𝐦𝐚𝐢𝐧! 📜
𝐒𝐞𝐞 𝐲𝐨𝐮 𝐬𝐨𝐨𝐧! 👋

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🌙━━━━━━━━━━━━━━━━━━━━━🌙
   🌟 {user} 🌟
   𝐌𝐎𝐎𝐍𝐋𝐈𝐆𝐇𝐓!
🌙━━━━━━━━━━━━━━━━━━━━━🌙

𝐓𝐡𝐞 𝐦𝐨𝐨𝐧 𝐫𝐢𝐬𝐞𝐬! 🌙
𝐓𝐡𝐞 𝐬𝐭𝐚𝐫 𝐟𝐚𝐥𝐥𝐬! 🌟
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 🌌

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """♾️━━━━━━━━━━━━━━━━━━━━━♾️
   🌈 {user} 🌈
   𝐄𝐍𝐃𝐋𝐄𝐒𝐒!
♾️━━━━━━━━━━━━━━━━━━━━━♾️

𝐓𝐡𝐞 𝐣𝐨𝐮𝐫𝐧𝐞𝐲 𝐞𝐧𝐝𝐬! 🚶
𝐁𝐮𝐭 𝐦𝐞𝐦𝐨𝐫𝐢𝐞𝐬 𝐥𝐚𝐬𝐭! 💫
𝐅𝐢𝐧𝐝 𝐲𝐨𝐮𝐫 𝐫𝐚𝐢𝐧𝐛𝐨𝐰! 🌈

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """🦋━━━━━━━━━━━━━━━━━━━━━🦋
   🌺 {user} 🌺
   𝐁𝐔𝐓𝐓𝐄𝐑𝐅𝐋𝐘!
🦋━━━━━━━━━━━━━━━━━━━━━🦋

𝐒𝐩𝐫𝐞𝐚𝐝 𝐲𝐨𝐮𝐫 𝐰𝐢𝐧𝐠𝐬! 🦋
𝐅𝐥𝐲 𝐟𝐫𝐞𝐞! 🌸
𝐅𝐢𝐧𝐝 𝐧𝐞𝐰 𝐠𝐚𝐫𝐝𝐞𝐧𝐬! 🌻

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {time}  •  📅 {date}
━━━━━━━━━━━━━━━━━━━━━━━""",

    """✨━━━━━━━━━━━━━━━━━━━━━✨
   ☄️ {user} ☄️
   𝐒𝐓𝐀𝐑𝐃𝐔𝐒𝐓!
✨━━━━━━━━━━━━━━━━━━━━━✨

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

# ========== SEND NOTIFICATION ==========
async def send_premium_notification(chat_id, user_mention, message_template):
    try:
        time = get_current_time()
        date = get_current_date()
        
        msg_text = message_template.format(
            user=user_mention,
            time=time,
            date=date
        )
        
        emojis = ["🔥", "✨", "💎", "🌟", "🎉", "🚀", "👑", "💫"]
        footer = random.sample(emojis, 4)
        msg_text += f"\n\n{footer[0]} ᴘʀᴇᴍɪᴜᴍ {footer[1]} ᴜᴘᴅᴀᴛᴇ {footer[2]} ʙʏ {footer[3]} ʙᴏᴛ"
        
        video_data = get_random_video()
        
        if video_data and os.path.exists(video_data["path"]):
            await app.send_video(
                chat_id=chat_id,
                video=video_data["path"],
                caption=msg_text,
                supports_streaming=True
            )
            logger.info(f"📹 Video #{video_data['id']} sent")
        else:
            await app.send_message(chat_id=chat_id, text=msg_text)
            logger.info(f"📝 Message sent (no video)")
    except Exception as e:
        logger.error(f"❌ Error: {e}")

# ========== GROUP AUTO-ADD (ANY USER CAN USE) ==========
@app.on_message(filters.group & filters.command("addgroup"))
async def add_group_from_group(client, message: Message):
    try:
        chat_id = message.chat.id
        chat_name = message.chat.title or f"Group {chat_id}"
        
        groups = load_groups()
        if str(chat_id) in groups:
            await message.reply_text(
                f"""✅━━━━━━━━━━━━━━━━━━━━━✅
   ⚠️ **__𝗔𝗟𝗥𝗘𝗔𝗗𝗬 𝗔𝗗𝗗𝗘𝗗!__** ⚠️
✅━━━━━━━━━━━━━━━━━━━━━✅

📛 **__𝗡𝗔𝗠𝗘:__** `{chat_name}`
🆔 **__𝗜𝗗:__** `{chat_id}`
📅 **__𝗔𝗗𝗗𝗘𝗗:__** {groups[str(chat_id)]['added_at'][:16]}

🌟 **__𝗦𝗧𝗔𝗧𝗨𝗦:__** ✅ **__𝗔𝗖𝗧𝗜𝗩𝗘__**

━━━━━━━━━━━━━━━━━━━━━━━
🌌 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗔𝗖𝗧𝗜𝗩𝗘__** 🌌"""
            )
            return
        
        save_group(chat_id, chat_name)
        
        confirm_text = f"""✅━━━━━━━━━━━━━━━━━━━━━✅
   🎯 **__𝗚𝗥𝗢𝗨𝗣 𝗔𝗗𝗗𝗘𝗗!__** 🎯
✅━━━━━━━━━━━━━━━━━━━━━✅

📛 **__𝗡𝗔𝗠𝗘:__** `{chat_name}`
🆔 **__𝗜𝗗:__** `{chat_id}`
📅 **__𝗗𝗔𝗧𝗘:__** {get_current_date()}
🕐 **__𝗧𝗜𝗠𝗘:__** {get_current_time()}

🌟 **__𝗦𝗧𝗔𝗧𝗨𝗦:__** ✅ **__𝗔𝗖𝗧𝗜𝗩𝗘__**

👤 **__𝗝𝗼𝗶𝗻__** │ 🚶 **__𝗟𝗲𝗮𝘃𝗲__** │ 🚫 **__𝗕𝗮𝗻__**

━━━━━━━━━━━━━━━━━━━━━━━
🌌 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗘𝗡𝗔𝗕𝗟𝗘𝗗__** 🌌"""

        sent_msg = await message.reply_text(confirm_text)
        
        await asyncio.sleep(5)
        try:
            await sent_msg.delete()
            await message.delete()
        except:
            pass
        
        logger.info(f"✅ Group auto-added: {chat_name}")
        
    except Exception as e:
        await message.reply_text(f"❌ **__Error:__** {str(e)}")

# ========== SERVICE MESSAGES ==========
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
                    random.choice(JOIN_MESSAGES)
                )
                logger.info(f"👤 JOIN: {user.first_name}")
        
        elif message.left_chat_member:
            user = message.left_chat_member
            if user.is_bot:
                return
                
            mention = f"[{user.first_name}](tg://user?id={user.id})"
            
            if hasattr(message, 'new_chat_members') and message.new_chat_members is None:
                await send_premium_notification(
                    chat_id,
                    mention,
                    random.choice(BAN_MESSAGES)
                )
                logger.info(f"🚫 BANNED: {user.first_name}")
            else:
                await send_premium_notification(
                    chat_id,
                    mention,
                    random.choice(LEFT_MESSAGES)
                )
                logger.info(f"🚶 LEFT: {user.first_name}")
                
    except Exception as e:
        logger.error(f"❌ Error: {e}")

# ========== START COMMAND ==========
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    if not is_owner(message.from_user.id):
        await message.reply_text(
            f"""❌━━━━━━━━━━━━━━━━━━━━━❌
   ⛔️ **__𝗨𝗡𝗔𝗨𝗧𝗛𝗢𝗥𝗜𝗭𝗘𝗗!__** ⛔️
❌━━━━━━━━━━━━━━━━━━━━━❌

**__𝗛𝗲𝘆__** {message.from_user.first_name}! 👋

𝐓𝐡𝐢𝐬 𝐛𝐨𝐭 𝐢𝐬 𝐨𝐧𝐥𝐲 𝐟𝐨𝐫 𝐭𝐡𝐞 𝐨𝐰𝐧𝐞𝐫! 🚫
𝐏𝐥𝐞𝐚𝐬𝐞 𝐝𝐨𝐧'𝐭 𝐭𝐫𝐲 𝐭𝐨 𝐮𝐬𝐞! ❌

𝐈𝐟 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐚𝐝𝐝 𝐭𝐡𝐢𝐬 𝐛𝐨𝐭 𝐭𝐨 𝐲𝐨𝐮𝐫 𝐠𝐫𝐨𝐮𝐩, 📌
𝐂𝐨𝐧𝐭𝐚𝐜𝐭 **__𝐁𝐄𝐒𝐓 𝘾𝙃𝙀𝘼𝙏 ᵒʷⁿᵉʳ__** 💬

━━━━━━━━━━━━━━━━━━━━━━━
🕐 {get_current_time()}  •  📅 {get_current_date()}
━━━━━━━━━━━━━━━━━━━━━━━
🚫 **__𝗥𝗘𝗦𝗧𝗥𝗜𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗘𝗦𝗦__** 🚫""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📩 ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}")]
            ])
        )
        return
    
    await message.reply_text(
        f"""💎━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💎
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    💎 **__ᴘʀᴇᴍɪᴜᴍ ʙᴏᴛ__** 💎     
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
💎━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💎

**__ʜᴇʏ__** {message.from_user.first_name}! 🌟  
**__ʙᴏᴛ ɪs ʀᴜɴɴɪɴɢ sᴍᴏᴏᴛʜʟʏ__** ✨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📹 **__ᴠɪᴅᴇᴏs:__** `{get_video_count()}`
👥 **__ɢʀᴏᴜᴘs:__** `{len(get_all_groups())}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📹 **__/addvideo__** - **__ᴀᴅᴅ__**
📋 **__/videos__** - **__ᴠɪᴇᴡ__**
🗑️ **__/delvideo__** - **__ᴅᴇʟ__**
🧹 **__/clearvideos__** - **__ᴄʟᴇᴀʀ__**

➕ **__/addgroup__** - **__ᴀᴅᴅ__**
📋 **__/groups__** - **__ᴠɪᴇᴡ__**
❌ **__/delgroup__** - **__ʀᴇᴍ__**
🔄 **__/toggle__** - **__ᴛᴏɢɢʟᴇ__**

📊 **__/stats__** - **__sᴛᴀᴛs__**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 **__ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴇ__** 💎
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    )

# ========== ADD GROUP PRIVATE (OWNER ONLY) ==========
@app.on_message(filters.command("addgroup") & filters.private)
async def add_group_private(client, message):
    if not is_owner(message.from_user.id):
        await message.reply_text("❌ **__Unauthorized!__**")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply_text(
                f"""❌━━━━━━━━━━━━━━━━━━━━━❌
   ⚠️ **__𝗜𝗡𝗩𝗔𝗟𝗜𝗗 𝗨𝗦𝗔𝗚𝗘!__** ⚠️
❌━━━━━━━━━━━━━━━━━━━━━❌

**__𝗨𝗦𝗔𝗚𝗘:__**
`/addgroup -100123456789`

**__𝗢𝗥__**
𝐓𝐲𝐩𝐞 `/addgroup` 𝐢𝐧 𝐚𝐧𝐲 𝐠𝐫𝐨𝐮𝐩
𝐓𝐨 𝐚𝐮𝐭𝐨-𝐚𝐝𝐝 𝐭𝐡𝐚𝐭 𝐠𝐫𝐨𝐮𝐩! ✅

━━━━━━━━━━━━━━━━━━━━━━━
💎 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧__** 💎
━━━━━━━━━━━━━━━━━━━━━━━"""
            )
            return
        
        group_id = int(parts[1])
        group_name = parts[2] if len(parts) > 2 else f"Group {group_id}"
        
        save_group(group_id, group_name)
        await message.reply_text(
            f"""✅━━━━━━━━━━━━━━━━━━━━━✅
   🎯 **__𝗚𝗥𝗢𝗨𝗣 𝗔𝗗𝗗𝗘𝗗!__** 🎯
✅━━━━━━━━━━━━━━━━━━━━━✅

📛 **__𝗡𝗔𝗠𝗘:__** `{group_name}`
🆔 **__𝗜𝗗:__** `{group_id}`
📅 **__𝗗𝗔𝗧𝗘:__** {get_current_date()}
🕐 **__𝗧𝗜𝗠𝗘:__** {get_current_time()}

🌟 **__𝗦𝗧𝗔𝗧𝗨𝗦:__** ✅ **__𝗔𝗖𝗧𝗜𝗩𝗘__**

━━━━━━━━━━━━━━━━━━━━━━━
💎 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗘𝗡𝗔𝗕𝗟𝗘𝗗__** 💎
━━━━━━━━━━━━━━━━━━━━━━━"""
        )
    except Exception as e:
        await message.reply_text(f"❌ **__Error:__** {str(e)}")

# ========== GROUPS LIST ==========
@app.on_message(filters.command("groups") & filters.private)
async def groups_list(client, message):
    if not is_owner(message.from_user.id):
        return
    
    groups = get_all_groups()
    if not groups:
        await message.reply_text(
            f"""❌━━━━━━━━━━━━━━━━━━━━━❌
   📭 **__𝗡𝗢 𝗚𝗥𝗢𝗨𝗣𝗦!__** 📭
❌━━━━━━━━━━━━━━━━━━━━━❌

𝐍𝐨 𝐠𝐫𝐨𝐮𝐩𝐬 𝐚𝐝𝐝𝐞𝐝 𝐲𝐞𝐭! 📌
𝐔𝐬𝐞 `/addgroup` 𝐭𝐨 𝐚𝐝𝐝! ✅

━━━━━━━━━━━━━━━━━━━━━━━
💎 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧__** 💎
━━━━━━━━━━━━━━━━━━━━━━━"""
        )
        return
    
    text = "👥 **__𝗠𝗬 𝗚𝗥𝗢𝗨𝗣𝗦__**\n\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━\n"
    for group_id, data in groups.items():
        status = "✅" if data.get("enabled", True) else "❌"
        text += f"{status} **__{data['name']}__**\n"
        text += f"🆔 `{group_id}`\n"
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
            await message.reply_text("❌ **__/delgroup -100123456789__**")
            return
        
        group_id = int(parts[1])
        if remove_group(group_id):
            await message.reply_text(f"✅ **__Group removed!__**")
        else:
            await message.reply_text(f"❌ **__Not found!__**")
    except:
        await message.reply_text("❌ **__Invalid!__**")

# ========== TOGGLE GROUP ==========
@app.on_message(filters.command("toggle") & filters.private)
async def toggle_group_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text("❌ **__/toggle -100123456789__**")
            return
        
        group_id = int(parts[1])
        status = toggle_group(group_id)
        await message.reply_text(
            f"""✅━━━━━━━━━━━━━━━━━━━━━✅
   🔄 **__𝗚𝗥𝗢𝗨𝗣 𝗧𝗢𝗚𝗚𝗟𝗘𝗗!__** 🔄
✅━━━━━━━━━━━━━━━━━━━━━✅

🆔 `{group_id}`
📊 **__𝗦𝗧𝗔𝗧𝗨𝗦:__** {'✅ **__Enabled__**' if status else '❌ **__Disabled__**'}

━━━━━━━━━━━━━━━━━━━━━━━
💎 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧__** 💎
━━━━━━━━━━━━━━━━━━━━━━━"""
        )
    except:
        await message.reply_text("❌ **__Invalid!__**")

# ========== ADD VIDEO ==========
@app.on_message(filters.command("addvideo") & filters.private)
async def add_video_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    status = await message.reply_text("⏳ **__Downloading...__**")
    
    try:
        if message.reply_to_message and message.reply_to_message.video:
            video_path = await message.reply_to_message.download()
            video_id = save_video(video_path)
            await status.edit_text(
                f"""✅━━━━━━━━━━━━━━━━━━━━━✅
   📹 **__VIDEO SAVED!__** 📹
✅━━━━━━━━━━━━━━━━━━━━━✅

🆔 **__ID:__** `{video_id}`
📹 **__Total:__** `{get_video_count()}`

━━━━━━━━━━━━━━━━━━━━━━━
💎 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧__** 💎
━━━━━━━━━━━━━━━━━━━━━━━"""
            )
        else:
            await status.edit_text(
                f"""❌━━━━━━━━━━━━━━━━━━━━━❌
   ⚠️ **__NO VIDEO!__** ⚠️
❌━━━━━━━━━━━━━━━━━━━━━❌

𝐏𝐥𝐞𝐚𝐬𝐞 𝐫𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐯𝐢𝐝𝐞𝐨! 📹

**__Usage:__** Send video
Then reply with `/addvideo`

━━━━━━━━━━━━━━━━━━━━━━━
💎 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧__** 💎
━━━━━━━━━━━━━━━━━━━━━━━"""
            )
    except Exception as e:
        await status.edit_text(f"❌ **__Error:__** {str(e)}")

# ========== VIDEOS LIST ==========
@app.on_message(filters.command("videos") & filters.private)
async def list_videos(client, message):
    if not is_owner(message.from_user.id):
        return
    
    videos = load_videos()
    if not videos:
        await message.reply_text(
            f"""❌━━━━━━━━━━━━━━━━━━━━━❌
   📭 **__NO VIDEOS!__** 📭
❌━━━━━━━━━━━━━━━━━━━━━❌

𝐍𝐨 𝐯𝐢𝐝𝐞𝐨𝐬 𝐢𝐧 𝐥𝐢𝐛𝐫𝐚𝐫𝐲! 📌
𝐔𝐬𝐞 `/addvideo` 𝐭𝐨 𝐚𝐝𝐝! ✅

━━━━━━━━━━━━━━━━━━━━━━━
💎 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧__** 💎
━━━━━━━━━━━━━━━━━━━━━━━"""
        )
        return
    
    text = "🎬 **__VIDEO LIBRARY__**\n\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━\n"
    for video in videos:
        used = "✅" if video.get("used", False) else "🔄"
        text += f"{used} #{video['id']} {video['name']}\n"
        text += "━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    text += f"\n📹 **__Total:__** `{len(videos)}`"
    await message.reply_text(text)

# ========== DELETE VIDEO ==========
@app.on_message(filters.command("delvideo") & filters.private)
async def delete_video_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text("❌ **__/delvideo 1__**")
            return
        
        video_id = int(parts[1])
        if delete_video_by_id(video_id):
            await message.reply_text(f"✅ **__Video #{video_id} deleted!__**")
        else:
            await message.reply_text(f"❌ **__Not found!__**")
    except:
        await message.reply_text("❌ **__Invalid!__**")

# ========== CLEAR VIDEOS ==========
@app.on_message(filters.command("clearvideos") & filters.private)
async def clear_videos_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    videos = load_videos()
    if not videos:
        await message.reply_text("❌ **__No videos!__**")
        return
    
    for video in videos:
        if os.path.exists(video["path"]):
            os.remove(video["path"])
    
    with open(VIDEO_DB, "w") as f:
        json.dump([], f)
    
    await message.reply_text(
        f"""✅━━━━━━━━━━━━━━━━━━━━━✅
   🗑️ **__ALL CLEARED!__** 🗑️
✅━━━━━━━━━━━━━━━━━━━━━✅

📹 **__Removed:__** `{len(videos)}` videos

━━━━━━━━━━━━━━━━━━━━━━━
💎 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗕𝗢𝗧__** 💎
━━━━━━━━━━━━━━━━━━━━━━━"""
    )

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
    
    text = f"""📊 **__𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗦__**

━━━━━━━━━━━━━━━━━━━━━━━
📹 **__Videos:__** `{len(videos)}`
🔄 **__Unused:__** `{len(videos) - used}`
✅ **__Used:__** `{used}`
💾 **__Size:__** `{total_size / (1024*1024):.2f}` MB

👥 **__Groups:__** `{len(groups)}`
✅ **__Enabled:__** `{sum(1 for g in groups.values() if g.get('enabled', True))}`

⏰ **__Uptime:__** `{datetime.now(IST).strftime('%d %b %Y %I:%M %p')}`
━━━━━━━━━━━━━━━━━━━━━━━
💎 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗔𝗖𝗧𝗜𝗩𝗘__** 💎
━━━━━━━━━━━━━━━━━━━━━━━"""
    
    await message.reply_text(text)

# ========== RUN ==========
if __name__ == "__main__":
    print("\n" + "="*40)
    print("🚀 PREMIUM BOT STARTING...")
    print("🐉 DRAGON THEME ACTIVE")
    print("="*40 + "\n")
    
    if not os.path.exists(VIDEO_DB):
        with open(VIDEO_DB, "w") as f:
            json.dump([], f)
    
    if not os.path.exists(GROUPS_DB):
        with open(GROUPS_DB, "w") as f:
            json.dump({}, f)
    
    os.makedirs("downloads", exist_ok=True)
    
    print(f"📹 Videos: {get_video_count()}")
    print(f"👥 Groups: {len(get_all_groups())}")
    print("\n" + "="*40)
    print("🤖 BOT IS RUNNING!")
    print("🐉 HAR BAAR NAYI VIDEO!")
    print("="*40 + "\n")
    
    try:
        app.run()
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
