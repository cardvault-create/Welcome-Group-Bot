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

# ========== 🔴 APNA DATA DAALO ==========
API_ID = 35140329
API_HASH = "011f638e4acadee178c59afffc80193d"
BOT_TOKEN = "8603632286:AAE8Hw5xWzKjrpr4r7PrrMifZxu7-v93TaM"
OWNER_ID = 7614459746

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
    return datetime.now(IST).strftime("%I:%M %p")

def get_current_date():
    return datetime.now(IST).strftime("%d %b %Y")

# ========== JOIN MESSAGES ==========
JOIN_MESSAGES = [
    """👑━━━━━━━━━━━━━━━━━━━━━👑
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🦁 {user} 🦁
┃ 𝐊𝐈𝐍𝐆 𝐖𝐄𝐋𝐂𝐎𝐌𝐄
┗━━━━━━━━━━━━━━━━━━━━━┛
👑━━━━━━━━━━━━━━━━━━━━━👑

𝐓𝐡𝐞 𝐤𝐢𝐧𝐠 𝐢𝐬 𝐡𝐞𝐫𝐞! 👑
𝐘𝐨𝐮'𝐫𝐞 𝐭𝐡𝐞 𝐫𝐮𝐥𝐞𝐫! ⚔️

🕐 {time} │ 📅 {date}""",

    """🔥━━━━━━━━━━━━━━━━━━━━━🔥
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🐦‍🔥 {user} 🐦‍🔥
┃ 𝐏𝐇𝐎𝐄𝐍𝐈𝐗 𝐑𝐈𝐒𝐄𝐒
┗━━━━━━━━━━━━━━━━━━━━━┛
🔥━━━━━━━━━━━━━━━━━━━━━🔥

𝐑𝐢𝐬𝐢𝐧𝐠 𝐟𝐫𝐨𝐦 𝐚𝐬𝐡! 🔥
𝐘𝐨𝐮'𝐫𝐞 𝐮𝐧𝐬𝐭𝐨𝐩𝐩𝐚𝐛𝐥𝐞! 💪

🕐 {time} │ 📅 {date}""",

    """🐉━━━━━━━━━━━━━━━━━━━━━🐉
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚡ {user} ⚡
┃ 𝐃𝐑𝐀𝐆𝐎𝐍 𝐀𝐑𝐑𝐈𝐕𝐄𝐃
┗━━━━━━━━━━━━━━━━━━━━━┛
🐉━━━━━━━━━━━━━━━━━━━━━🐉

𝐃𝐫𝐚𝐠𝐨𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞! 🐲
𝐔𝐧𝐥𝐞𝐚𝐬𝐡 𝐭𝐡𝐞 𝐩𝐨𝐰𝐞𝐫! ⚡

🕐 {time} │ 📅 {date}""",

    """🐺━━━━━━━━━━━━━━━━━━━━━🐺
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🌙 {user} 🌙
┃ 𝐋𝐄𝐆𝐄𝐍𝐃 𝐉𝐎𝐈𝐍𝐒
┗━━━━━━━━━━━━━━━━━━━━━┛
🐺━━━━━━━━━━━━━━━━━━━━━🐺

𝐖𝐨𝐥𝐟 𝐡𝐚𝐬 𝐚𝐫𝐫𝐢𝐯𝐞𝐝! 🌕
𝐋𝐞𝐚𝐝𝐞𝐫 𝐨𝐟 𝐭𝐡𝐞 𝐩𝐚𝐜𝐤! 🐾

🕐 {time} │ 📅 {date}""",

    """💪━━━━━━━━━━━━━━━━━━━━━💪
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🦍 {user} 🦍
┃ 𝐓𝐈𝐓𝐀𝐍 𝐀𝐑𝐑𝐈𝐕𝐄𝐃
┗━━━━━━━━━━━━━━━━━━━━━┛
💪━━━━━━━━━━━━━━━━━━━━━💪

𝐓𝐢𝐭𝐚𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞! 🏔️
𝐒𝐭𝐫𝐞𝐧𝐠𝐭𝐡 𝐮𝐧𝐥𝐞𝐚𝐬𝐡𝐞𝐝! ⚡

🕐 {time} │ 📅 {date}""",

    """🌌━━━━━━━━━━━━━━━━━━━━━🌌
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🚀 {user} 🚀
┃ 𝐆𝐀𝐋𝐀𝐗𝐘 𝐉𝐎𝐈𝐍
┗━━━━━━━━━━━━━━━━━━━━━┛
🌌━━━━━━━━━━━━━━━━━━━━━🌌

𝐀 𝐬𝐭𝐚𝐫 𝐢𝐬 𝐛𝐨𝐫𝐧! 🌟
𝐓𝐡𝐞 𝐜𝐨𝐬𝐦𝐨𝐬 𝐰𝐚𝐢𝐭𝐬! 🌠

🕐 {time} │ 📅 {date}""",

    """🏯━━━━━━━━━━━━━━━━━━━━━🏯
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🐯 {user} 🐯
┃ 𝐄𝐌𝐏𝐄𝐑𝐎𝐑 𝐖𝐄𝐋𝐂𝐎𝐌𝐄
┗━━━━━━━━━━━━━━━━━━━━━┛
🏯━━━━━━━━━━━━━━━━━━━━━🏯

𝐄𝐦𝐩𝐞𝐫𝐨𝐫 𝐡𝐚𝐬 𝐚𝐫𝐫𝐢𝐯𝐞𝐝! 👑
𝐋𝐞𝐠𝐞𝐧𝐝 𝐛𝐞𝐠𝐢𝐧𝐬! 📜

🕐 {time} │ 📅 {date}""",

    """🦄━━━━━━━━━━━━━━━━━━━━━🦄
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ ✨ {user} ✨
┃ 𝐌𝐀𝐆𝐈𝐂 𝐉𝐎𝐈𝐍
┗━━━━━━━━━━━━━━━━━━━━━┛
🦄━━━━━━━━━━━━━━━━━━━━━🦄

𝐔𝐧𝐢𝐜𝐨𝐫𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞! 🦄
𝐌𝐚𝐠𝐢𝐜 𝐢𝐧 𝐭𝐡𝐞 𝐚𝐢𝐫! ✨

🕐 {time} │ 📅 {date}""",

    """🦈━━━━━━━━━━━━━━━━━━━━━🦈
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚓ {user} ⚓
┃ 𝐄𝐋𝐈𝐓𝐄 𝐀𝐑𝐑𝐈𝐕𝐄𝐃
┗━━━━━━━━━━━━━━━━━━━━━┛
🦈━━━━━━━━━━━━━━━━━━━━━🦈

𝐒𝐡𝐚𝐫𝐤 𝐢𝐬 𝐡𝐞𝐫𝐞! 🌊
𝐔𝐧𝐬𝐭𝐨𝐩𝐩𝐚𝐛𝐥𝐞 𝐟𝐨𝐫𝐜𝐞! 💪

🕐 {time} │ 📅 {date}""",

    """🦅━━━━━━━━━━━━━━━━━━━━━🦅
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ ☀️ {user} ☀️
┃ 𝐑𝐎𝐘𝐀𝐋 𝐅𝐋𝐘
┗━━━━━━━━━━━━━━━━━━━━━┛
🦅━━━━━━━━━━━━━━━━━━━━━🦅

𝐄𝐚𝐠𝐥𝐞 𝐡𝐚𝐬 𝐟𝐥𝐨𝐰𝐧! 🦅
𝐅𝐥𝐲 𝐡𝐢𝐠𝐡! 𝐃𝐫𝐞𝐚𝐦 𝐛𝐢𝐠! ☀️

🕐 {time} │ 📅 {date}"""
]

# ========== BAN MESSAGES ==========
BAN_MESSAGES = [
    """⚖️━━━━━━━━━━━━━━━━━━━━━⚖️
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ ⛔️ {user} ⛔️
┃ 𝐉𝐔𝐒𝐓𝐈𝐂𝐄 𝐒𝐄𝐑𝐕𝐄𝐃
┗━━━━━━━━━━━━━━━━━━━━━┛
⚖️━━━━━━━━━━━━━━━━━━━━━⚖️

𝐑𝐮𝐥𝐞𝐬 𝐰𝐞𝐫𝐞 𝐛𝐫𝐨𝐤𝐞𝐧! 🚨
𝐆𝐫𝐨𝐮𝐩 𝐢𝐬 𝐬𝐚𝐟𝐞! 🛡️

🕐 {time} │ 📅 {date}""",

    """🔨━━━━━━━━━━━━━━━━━━━━━🔨
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🚷 {user} 🚷
┃ 𝐁𝐀𝐍 𝐇𝐀𝐌𝐌𝐄𝐑
┗━━━━━━━━━━━━━━━━━━━━━┛
🔨━━━━━━━━━━━━━━━━━━━━━🔨

𝐎𝐮𝐭 𝐨𝐟 𝐭𝐡𝐞 𝐠𝐚𝐦𝐞! ⚽
𝐑𝐮𝐥𝐞𝐬 𝐚𝐫𝐞 𝐫𝐮𝐥𝐞𝐬! 📜

🕐 {time} │ 📅 {date}""",

    """🚀━━━━━━━━━━━━━━━━━━━━━🚀
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 💢 {user} 💢
┃ 𝐄𝐉𝐄𝐂𝐓𝐄𝐃
┗━━━━━━━━━━━━━━━━━━━━━┛
🚀━━━━━━━━━━━━━━━━━━━━━🚀

𝐘𝐨𝐮'𝐫𝐞 𝐨𝐮𝐭! 🌌
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

🕐 {time} │ 📅 {date}""",

    """🔒━━━━━━━━━━━━━━━━━━━━━🔒
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🚷 {user} 🚷
┃ 𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 𝐋𝐎𝐂𝐊
┗━━━━━━━━━━━━━━━━━━━━━┛
🔒━━━━━━━━━━━━━━━━━━━━━🔒

𝐀𝐜𝐜𝐞𝐬𝐬 𝐝𝐞𝐧𝐢𝐞𝐝! 🚫
𝐒𝐚𝐟𝐞 𝐬𝐩𝐚𝐜𝐞 𝐦𝐚𝐢𝐧𝐭𝐚𝐢𝐧𝐞𝐝! ✨

🕐 {time} │ 📅 {date}""",

    """🚫━━━━━━━━━━━━━━━━━━━━━🚫
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ ⛔️ {user} ⛔️
┃ 𝐎𝐔𝐓𝐂𝐀𝐒𝐓
┗━━━━━━━━━━━━━━━━━━━━━┛
🚫━━━━━━━━━━━━━━━━━━━━━🚫

𝐍𝐨 𝐦𝐨𝐫𝐞 𝐜𝐡𝐚𝐧𝐜𝐞𝐬! ❌
𝐓𝐢𝐦𝐞 𝐭𝐨 𝐠𝐨! 🚪

🕐 {time} │ 📅 {date}""",

    """💀━━━━━━━━━━━━━━━━━━━━━💀
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ ⚡ {user} ⚡
┃ 𝐓𝐄𝐑𝐌𝐈𝐍𝐀𝐓𝐄𝐃
┗━━━━━━━━━━━━━━━━━━━━━┛
💀━━━━━━━━━━━━━━━━━━━━━💀

𝐆𝐚𝐦𝐞 𝐨𝐯𝐞𝐫! 🎮
𝐓𝐡𝐞 𝐞𝐧𝐝! 💥

🕐 {time} │ 📅 {date}""",

    """🗡️━━━━━━━━━━━━━━━━━━━━━🗡️
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 💢 {user} 💢
┃ 𝐁𝐀𝐍𝐈𝐒𝐇𝐄𝐃
┗━━━━━━━━━━━━━━━━━━━━━┛
🗡️━━━━━━━━━━━━━━━━━━━━━🗡️

𝐅𝐨𝐫𝐞𝐯𝐞𝐫 𝐠𝐨𝐧𝐞! 🌅
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

🕐 {time} │ 📅 {date}""",

    """🔐━━━━━━━━━━━━━━━━━━━━━🔐
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🚷 {user} 🚷
┃ 𝐁𝐋𝐎𝐂𝐊𝐄𝐃
┗━━━━━━━━━━━━━━━━━━━━━┛
🔐━━━━━━━━━━━━━━━━━━━━━🔐

𝐍𝐨 𝐞𝐧𝐭𝐫𝐲! 🚪
𝐌𝐨𝐯𝐞 𝐨𝐧! 🚶

🕐 {time} │ 📅 {date}""",

    """🎯━━━━━━━━━━━━━━━━━━━━━🎯
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ ⛔️ {user} ⛔️
┃ 𝐄𝐗𝐏𝐄𝐋𝐋𝐄𝐃
┗━━━━━━━━━━━━━━━━━━━━━┛
🎯━━━━━━━━━━━━━━━━━━━━━🎯

𝐓𝐚𝐫𝐠𝐞𝐭 𝐫𝐞𝐦𝐨𝐯𝐞𝐝! 🎯
𝐍𝐨 𝐦𝐞𝐫𝐜𝐲! ❌

🕐 {time} │ 📅 {date}""",

    """💥━━━━━━━━━━━━━━━━━━━━━💥
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 💢 {user} 💢
┃ 𝐔𝐋𝐓𝐈𝐌𝐀𝐓𝐄 𝐁𝐀𝐍
┗━━━━━━━━━━━━━━━━━━━━━┛
💥━━━━━━━━━━━━━━━━━━━━━💥

𝐅𝐢𝐧𝐚𝐥 𝐬𝐭𝐫𝐢𝐤𝐞! ⚡
𝐈𝐭'𝐬 𝐨𝐯𝐞𝐫! 🎬

🕐 {time} │ 📅 {date}"""
]

# ========== LEFT MESSAGES ==========
LEFT_MESSAGES = [
    """👋━━━━━━━━━━━━━━━━━━━━━👋
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 💔 {user} 💔
┃ 𝐆𝐎𝐎𝐃𝐁𝐘𝐄
┗━━━━━━━━━━━━━━━━━━━━━┛
👋━━━━━━━━━━━━━━━━━━━━━👋

𝐖𝐞'𝐥𝐥 𝐦𝐢𝐬𝐬 𝐲𝐨𝐮! 🥺
𝐓𝐚𝐤𝐞 𝐜𝐚𝐫𝐞! 🌈

🕐 {time} │ 📅 {date}""",

    """🚶━━━━━━━━━━━━━━━━━━━━━🚶
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🌅 {user} 🌅
┃ 𝐃𝐄𝐏𝐀𝐑𝐓𝐔𝐑𝐄
┗━━━━━━━━━━━━━━━━━━━━━┛
🚶━━━━━━━━━━━━━━━━━━━━━🚶

𝐖𝐚𝐥𝐤𝐢𝐧𝐠 𝐚𝐰𝐚𝐲! 🚶
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

🕐 {time} │ 📅 {date}""",

    """🕊️━━━━━━━━━━━━━━━━━━━━━🕊️
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 💫 {user} 💫
┃ 𝐋𝐎𝐒𝐓 𝐒𝐎𝐔𝐋
┗━━━━━━━━━━━━━━━━━━━━━┛
🕊️━━━━━━━━━━━━━━━━━━━━━🕊️

𝐅𝐥𝐲 𝐡𝐢𝐠𝐡! 🕊️
𝐘𝐨𝐮'𝐥𝐥 𝐛𝐞 𝐦𝐢𝐬𝐬𝐞𝐝! 💔

🕐 {time} │ 📅 {date}""",

    """🌊━━━━━━━━━━━━━━━━━━━━━🌊
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🚣 {user} 🚣
┃ 𝐌𝐎𝐕𝐈𝐍𝐆 𝐎𝐍
┗━━━━━━━━━━━━━━━━━━━━━┛
🌊━━━━━━━━━━━━━━━━━━━━━🌊

𝐒𝐚𝐢𝐥𝐢𝐧𝐠 𝐚𝐰𝐚𝐲! ⛵
𝐓𝐡𝐞 𝐬𝐞𝐚 𝐰𝐚𝐢𝐭𝐬! 🌊

🕐 {time} │ 📅 {date}""",

    """✌️━━━━━━━━━━━━━━━━━━━━━✌️
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ ☮️ {user} ☮️
┃ 𝐏𝐄𝐀𝐂𝐄 𝐎𝐔𝐓
┗━━━━━━━━━━━━━━━━━━━━━┛
✌️━━━━━━━━━━━━━━━━━━━━━✌️

𝐒𝐩𝐫𝐞𝐚𝐝 𝐥𝐨𝐯𝐞! ❤️
𝐓𝐚𝐤𝐞 𝐜𝐚𝐫𝐞! ✌️

🕐 {time} │ 📅 {date}""",

    """🌹━━━━━━━━━━━━━━━━━━━━━🌹
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🥀 {user} 🥀
┃ 𝐅𝐀𝐑𝐄𝐖𝐄𝐋𝐋
┗━━━━━━━━━━━━━━━━━━━━━┛
🌹━━━━━━━━━━━━━━━━━━━━━🌹

𝐀 𝐫𝐨𝐬𝐞 𝐡𝐚𝐬 𝐟𝐚𝐥𝐥𝐞𝐧! 🌹
𝐒𝐞𝐞 𝐲𝐨𝐮 𝐬𝐨𝐨𝐧! 👋

🕐 {time} │ 📅 {date}""",

    """🌙━━━━━━━━━━━━━━━━━━━━━🌙
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🌟 {user} 🌟
┃ 𝐌𝐎𝐎𝐍𝐋𝐈𝐆𝐇𝐓
┗━━━━━━━━━━━━━━━━━━━━━┛
🌙━━━━━━━━━━━━━━━━━━━━━🌙

𝐓𝐡𝐞 𝐦𝐨𝐨𝐧 𝐫𝐢𝐬𝐞𝐬! 🌙
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 🌌

🕐 {time} │ 📅 {date}""",

    """♾️━━━━━━━━━━━━━━━━━━━━━♾️
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🌈 {user} 🌈
┃ 𝐄𝐍𝐃𝐋𝐄𝐒𝐒
┗━━━━━━━━━━━━━━━━━━━━━┛
♾️━━━━━━━━━━━━━━━━━━━━━♾️

𝐌𝐞𝐦𝐨𝐫𝐢𝐞𝐬 𝐥𝐚𝐬𝐭! 💫
𝐅𝐢𝐧𝐝 𝐲𝐨𝐮𝐫 𝐫𝐚𝐢𝐧𝐛𝐨𝐰! 🌈

🕐 {time} │ 📅 {date}""",

    """🦋━━━━━━━━━━━━━━━━━━━━━🦋
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🌺 {user} 🌺
┃ 𝐁𝐔𝐓𝐓𝐄𝐑𝐅𝐋𝐘
┗━━━━━━━━━━━━━━━━━━━━━┛
🦋━━━━━━━━━━━━━━━━━━━━━🦋

𝐒𝐩𝐫𝐞𝐚𝐝 𝐰𝐢𝐧𝐠𝐬! 🦋
𝐅𝐥𝐲 𝐟𝐫𝐞𝐞! 🌸

🕐 {time} │ 📅 {date}""",

    """✨━━━━━━━━━━━━━━━━━━━━━✨
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ ☄️ {user} ☄️
┃ 𝐒𝐓𝐀𝐑𝐃𝐔𝐒𝐓
┗━━━━━━━━━━━━━━━━━━━━━┛
✨━━━━━━━━━━━━━━━━━━━━━✨

𝐀 𝐬𝐭𝐚𝐫 𝐡𝐚𝐬 𝐠𝐨𝐧𝐞! 🌟
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

🕐 {time} │ 📅 {date}"""
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
        
        emojis = ["🔥", "✨", "💎", "🌟", "🎉", "🚀"]
        footer = random.sample(emojis, 3)
        msg_text += f"\n\n{footer[0]} ᴘʀᴇᴍɪᴜᴍ {footer[1]} ᴜᴘᴅᴀᴛᴇ {footer[2]}"
        
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

# ========== GROUP AUTO-ADD ==========
@app.on_message(filters.group & filters.command("addgroup") & filters.user(OWNER_ID))
async def add_group_from_group(client, message: Message):
    try:
        chat_id = message.chat.id
        chat_name = message.chat.title or f"Group {chat_id}"
        
        save_group(chat_id, chat_name)
        
        confirm_text = f"""✅━━━━━━━━━━━━━━━━━━━━━✅
┏━━━━━━━━━━━━━━━━━━━━━┓
┃ 🎯 𝗚𝗥𝗢𝗨𝗣 𝗔𝗗𝗗𝗘𝗗 🎯
┗━━━━━━━━━━━━━━━━━━━━━┛
✅━━━━━━━━━━━━━━━━━━━━━✅

📛 𝗡𝗔𝗠𝗘: `{chat_name}`
🆔 𝗜𝗗: `{chat_id}`
📅 {get_current_date()}
🕐 {get_current_time()}

🌟 𝗦𝗧𝗔𝗧𝗨𝗦: ✅ 𝗔𝗖𝗧𝗜𝗩𝗘
👤𝗝𝗼𝗶𝗻 │ 🚶𝗟𝗲𝗮𝘃𝗲 │ 🚫𝗕𝗮𝗻

━━━━━━━━━━━━━━━━━━━━━
🌌 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗘𝗡𝗔𝗕𝗟𝗘𝗗 🌌"""

        sent_msg = await message.reply_text(confirm_text)
        
        await asyncio.sleep(5)
        try:
            await sent_msg.delete()
            await message.delete()
        except:
            pass
        
        logger.info(f"✅ Group auto-added: {chat_name}")
        
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

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
        await message.reply_text("❌ Unauthorized!")
        return
    
    await message.reply_text(
        f"""💎━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💎
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃    💎 ᴘʀᴇᴍɪᴜᴍ ʙᴏᴛ 💎     
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
💎━━━━━━━━━━━━━━━━━━━━━━━━━━━━━💎

ʜᴇʏ **{message.from_user.first_name}**! 🌟  
ʙᴏᴛ ɪs ʀᴜɴɴɪɴɢ sᴍᴏᴏᴛʜʟʏ ✨

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📹 **ᴠɪᴅᴇᴏs:** `{get_video_count()}`
👥 **ɢʀᴏᴜᴘs:** `{len(get_all_groups())}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📹 `/addvideo` - ᴀᴅᴅ
📋 `/videos` - ᴠɪᴇᴡ
🗑️ `/delvideo` - ᴅᴇʟ
🧹 `/clearvideos` - ᴄʟᴇᴀʀ

➕ `/addgroup` - ᴀᴅᴅ
📋 `/groups` - ᴠɪᴇᴡ
❌ `/delgroup` - ʀᴇᴍ
🔄 `/toggle` - ᴛᴏɢɢʟᴇ

📊 `/stats` - sᴛᴀᴛs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💎 **ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴇ** 💎
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    )

# ========== ADD GROUP PRIVATE ==========
@app.on_message(filters.command("addgroup") & filters.private)
async def add_group_private(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply_text("❌ /addgroup -100123456789")
            return
        
        group_id = int(parts[1])
        group_name = parts[2] if len(parts) > 2 else f"Group {group_id}"
        
        save_group(group_id, group_name)
        await message.reply_text(f"✅ Group added!\n📛 {group_name}\n🆔 {group_id}")
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# ========== GROUPS LIST ==========
@app.on_message(filters.command("groups") & filters.private)
async def groups_list(client, message):
    if not is_owner(message.from_user.id):
        return
    
    groups = get_all_groups()
    if not groups:
        await message.reply_text("❌ No groups!")
        return
    
    text = "👥 My Groups\n\n"
    for group_id, data in groups.items():
        status = "✅" if data.get("enabled", True) else "❌"
        text += f"{status} {data['name']}\n🆔 {group_id}\n\n"
    
    await message.reply_text(text)

# ========== DELETE GROUP ==========
@app.on_message(filters.command("delgroup") & filters.private)
async def delete_group(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text("❌ /delgroup -100123456789")
            return
        
        group_id = int(parts[1])
        if remove_group(group_id):
            await message.reply_text(f"✅ Group removed!")
        else:
            await message.reply_text(f"❌ Not found!")
    except:
        await message.reply_text("❌ Invalid!")

# ========== TOGGLE GROUP ==========
@app.on_message(filters.command("toggle") & filters.private)
async def toggle_group_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text("❌ /toggle -100123456789")
            return
        
        group_id = int(parts[1])
        status = toggle_group(group_id)
        await message.reply_text(f"✅ {group_id}\n📊 {'Enabled' if status else 'Disabled'}")
    except:
        await message.reply_text("❌ Invalid!")

# ========== ADD VIDEO ==========
@app.on_message(filters.command("addvideo") & filters.private)
async def add_video_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    status = await message.reply_text("⏳ Downloading...")
    
    try:
        if message.reply_to_message and message.reply_to_message.video:
            video_path = await message.reply_to_message.download()
            video_id = save_video(video_path)
            await status.edit_text(f"✅ Video #{video_id} saved!\n📹 Total: {get_video_count()}")
        else:
            await status.edit_text("❌ Reply to a video!")
    except Exception as e:
        await status.edit_text(f"❌ Error: {str(e)}")

# ========== VIDEOS LIST ==========
@app.on_message(filters.command("videos") & filters.private)
async def list_videos(client, message):
    if not is_owner(message.from_user.id):
        return
    
    videos = load_videos()
    if not videos:
        await message.reply_text("❌ No videos!")
        return
    
    text = "🎬 Videos\n\n"
    for video in videos:
        used = "✅" if video.get("used", False) else "🔄"
        text += f"{used} #{video['id']} {video['name']}\n"
    
    text += f"\n📹 Total: {len(videos)}"
    await message.reply_text(text)

# ========== DELETE VIDEO ==========
@app.on_message(filters.command("delvideo") & filters.private)
async def delete_video_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text("❌ /delvideo 1")
            return
        
        video_id = int(parts[1])
        if delete_video_by_id(video_id):
            await message.reply_text(f"✅ Video #{video_id} deleted!")
        else:
            await message.reply_text(f"❌ Not found!")
    except:
        await message.reply_text("❌ Invalid!")

# ========== CLEAR VIDEOS ==========
@app.on_message(filters.command("clearvideos") & filters.private)
async def clear_videos_command(client, message):
    if not is_owner(message.from_user.id):
        return
    
    videos = load_videos()
    if not videos:
        await message.reply_text("❌ No videos!")
        return
    
    for video in videos:
        if os.path.exists(video["path"]):
            os.remove(video["path"])
    
    with open(VIDEO_DB, "w") as f:
        json.dump([], f)
    
    await message.reply_text(f"🗑️ {len(videos)} cleared!")

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
    
    text = f"""📊 Stats

📹 Videos: {len(videos)}
🔄 Unused: {len(videos) - used}
✅ Used: {used}
💾 Size: {total_size / (1024*1024):.2f} MB

👥 Groups: {len(groups)}
✅ Enabled: {sum(1 for g in groups.values() if g.get('enabled', True))}

⏰ {datetime.now(IST).strftime('%d %b %Y %I:%M %p')}
━━━━━━━━━━━━━━━━━━━━━
💎 Premium Active 💎"""
    
    await message.reply_text(text)

# ========== RUN ==========
if __name__ == "__main__":
    print("\n" + "="*40)
    print("🚀 PREMIUM BOT STARTING...")
    print("💎 DIAMOND THEME ACTIVE")
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
    print("💎 HAR BAAR NAYI VIDEO!")
    print("="*40 + "\n")
    
    try:
        app.run()
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
