import asyncio
import json
import random
import os
import logging
from datetime import datetime, timedelta
import pytz
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions

# ========== LOGGING ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== 🔴 APNA DATA DAALO ==========
API_ID = 35140329
API_HASH = "011f638e4acadee178c59afffc80193d"
BOT_TOKEN = "8603632286:AAEK7TKZ-XLXTXUSniwqsHAZ1Fr89RPB1cU"
OWNER_ID = 7614459746
OWNER_USERNAME = "BESTCHEAT_OWNER"

# ========== DATABASE ==========
VIDEO_DB = "videos.json"
GROUPS_DB = "groups.json"
MUTE_DB = "mutes.json"
REVOKE_DB = "revoke.json"

# ========== TIMEZONE ==========
IST = pytz.timezone('Asia/Kolkata')

# ========== LINE SIZES ==========
LINE = "━━━━━━━━━━━━━━━━━"          # 15 dashes - normal lines
LINE_BIG = "━━━━━━━━━━━━━━━━━━━━━━━"  # 23 dashes - date lines

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

# ========== MUTE DATABASE ==========
def load_mutes():
    try:
        if os.path.exists(MUTE_DB):
            with open(MUTE_DB, "r") as f:
                return json.load(f)
    except:
        pass
    return {}

def save_mute(group_id, user_id, until):
    mutes = load_mutes()
    key = f"{group_id}_{user_id}"
    mutes[key] = until
    with open(MUTE_DB, "w") as f:
        json.dump(mutes, f, indent=2)

def remove_mute(group_id, user_id):
    mutes = load_mutes()
    key = f"{group_id}_{user_id}"
    if key in mutes:
        del mutes[key]
        with open(MUTE_DB, "w") as f:
            json.dump(mutes, f, indent=2)
        return True
    return False

def is_muted(group_id, user_id):
    mutes = load_mutes()
    key = f"{group_id}_{user_id}"
    if key in mutes:
        until = mutes[key]
        if until == "permanent":
            return True
        try:
            until_time = datetime.fromisoformat(until)
            if datetime.now() < until_time:
                return True
            else:
                remove_mute(group_id, user_id)
        except:
            remove_mute(group_id, user_id)
    return False

# ========== REVOKE DATABASE ==========
def load_revoke():
    try:
        if os.path.exists(REVOKE_DB):
            with open(REVOKE_DB, "r") as f:
                return json.load(f)
    except:
        pass
    return {}

def save_revoke(group_id, user_id):
    revoke = load_revoke()
    key = f"{group_id}_{user_id}"
    revoke[key] = True
    with open(REVOKE_DB, "w") as f:
        json.dump(revoke, f, indent=2)

def remove_revoke(group_id, user_id):
    revoke = load_revoke()
    key = f"{group_id}_{user_id}"
    if key in revoke:
        del revoke[key]
        with open(REVOKE_DB, "w") as f:
            json.dump(revoke, f, indent=2)
        return True
    return False

def is_revoked(group_id, user_id):
    revoke = load_revoke()
    key = f"{group_id}_{user_id}"
    return key in revoke

# ========== TIME FUNCTIONS ==========
def get_current_time():
    return datetime.now(IST).strftime("%I:%M:%S %p")

def get_current_date():
    return datetime.now(IST).strftime("%B %d, %Y")

def parse_time(time_str):
    if time_str.endswith('s'):
        return int(time_str[:-1]), "second"
    elif time_str.endswith('m'):
        return int(time_str[:-1]), "minute"
    elif time_str.endswith('h'):
        return int(time_str[:-1]), "hour"
    elif time_str.endswith('d'):
        return int(time_str[:-1]), "day"
    elif time_str.endswith('w'):
        return int(time_str[:-1]), "week"
    return None, None

# ========== SHORT MESSAGES ==========
JOIN_MSGS = [
    f"""🔥{LINE}🔥
   🐦‍🔥 {{user}} 🐦‍🔥
   𝐏𝐇𝐎𝐄𝐍𝐈𝐗 𝐑𝐈𝐒𝐄𝐒!
🔥{LINE}🔥

𝐑𝐢𝐬𝐢𝐧𝐠 𝐟𝐫𝐨𝐦 𝐚𝐬𝐡! 🔥
𝐘𝐨𝐮'𝐫𝐞 𝐮𝐧𝐬𝐭𝐨𝐩𝐩𝐚𝐛𝐥𝐞! 💪
𝐁𝐨𝐫𝐧 𝐭𝐨 𝐰𝐢𝐧! 🏆

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""👑{LINE}👑
   🦁 {{user}} 🦁
   𝐊𝐈𝐍𝐆 𝐖𝐄𝐋𝐂𝐎𝐌𝐄!
👑{LINE}👑

𝐓𝐡𝐞 𝐤𝐢𝐧𝐠 𝐢𝐬 𝐡𝐞𝐫𝐞! 👑
𝐘𝐨𝐮'𝐫𝐞 𝐭𝐡𝐞 𝐫𝐮𝐥𝐞𝐫! ⚔️
𝐋𝐞𝐭'𝐬 𝐜𝐨𝐧𝐪𝐮𝐞𝐫! 🏰

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🐉{LINE}🐉
   ⚡ {{user}} ⚡
   𝐃𝐑𝐀𝐆𝐎𝐍 𝐀𝐑𝐑𝐈𝐕𝐄𝐃!
🐉{LINE}🐉

𝐓𝐡𝐞 𝐝𝐫𝐚𝐠𝐨𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞! 🐲
𝐅𝐢𝐫𝐞 𝐢𝐧 𝐭𝐡𝐞 𝐬𝐨𝐮𝐥! 🔥
𝐔𝐧𝐥𝐞𝐚𝐬𝐡 𝐩𝐨𝐰𝐞𝐫! ⚡

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🐺{LINE}🐺
   🌙 {{user}} 🌙
   𝐋𝐄𝐆𝐄𝐍𝐃 𝐉𝐎𝐈𝐍𝐒!
🐺{LINE}🐺

𝐖𝐨𝐥𝐟 𝐡𝐚𝐬 𝐚𝐫𝐫𝐢𝐯𝐞𝐝! 🌕
𝐋𝐞𝐚𝐝𝐞𝐫 𝐨𝐟 𝐩𝐚𝐜𝐤! 🐾
𝐋𝐞𝐭'𝐬 𝐡𝐨𝐰𝐥! 🌙

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""💪{LINE}💪
   🦍 {{user}} 🦍
   𝐓𝐈𝐓𝐀𝐍 𝐀𝐑𝐑𝐈𝐕𝐄𝐃!
💪{LINE}💪

𝐓𝐢𝐭𝐚𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞! 🏔️
𝐒𝐭𝐫𝐞𝐧𝐠𝐭𝐡 𝐮𝐧𝐥𝐞𝐚𝐬𝐡! ⚡
𝐋𝐞𝐭'𝐬 𝐝𝐨𝐦𝐢𝐧𝐚𝐭𝐞! 🔥

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🌌{LINE}🌌
   🚀 {{user}} 🚀
   𝐆𝐀𝐋𝐀𝐗𝐘 𝐉𝐎𝐈𝐍!
🌌{LINE}🌌

𝐀 𝐬𝐭𝐚𝐫 𝐢𝐬 𝐛𝐨𝐫𝐧! 🌟
𝐁𝐞𝐲𝐨𝐧𝐝 𝐭𝐡𝐢𝐬 𝐰𝐨𝐫𝐥𝐝! 👽
𝐂𝐨𝐬𝐦𝐨𝐬 𝐰𝐚𝐢𝐭𝐬! 🌠

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🏯{LINE}🏯
   🐯 {{user}} 🐯
   𝐄𝐌𝐏𝐄𝐑𝐎𝐑 𝐖𝐄𝐋𝐂𝐎𝐌𝐄!
🏯{LINE}🏯

𝐄𝐦𝐩𝐞𝐫𝐨𝐫 𝐚𝐫𝐫𝐢𝐯𝐞𝐝! 👑
𝐑𝐞𝐬𝐩𝐞𝐜𝐭 𝐭𝐡𝐞 𝐜𝐫𝐨𝐰𝐧! ⚜️
𝐋𝐞𝐠𝐞𝐧𝐝 𝐛𝐞𝐠𝐢𝐧𝐬! 📜

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🦄{LINE}🦄
   ✨ {{user}} ✨
   𝐌𝐀𝐆𝐈𝐂 𝐉𝐎𝐈𝐍!
🦄{LINE}🦄

𝐔𝐧𝐢𝐜𝐨𝐫𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞! 🦄
𝐌𝐚𝐠𝐢𝐜 𝐢𝐧 𝐚𝐢𝐫! ✨
𝐎𝐧𝐞 𝐨𝐟 𝐚 𝐤𝐢𝐧𝐝! 💫

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🦈{LINE}🦈
   ⚓ {{user}} ⚓
   𝐄𝐋𝐈𝐓𝐄 𝐀𝐑𝐑𝐈𝐕𝐄𝐃!
🦈{LINE}🦈

𝐒𝐡𝐚𝐫𝐤 𝐢𝐬 𝐡𝐞𝐫𝐞! 🌊
𝐑𝐮𝐥𝐞 𝐭𝐡𝐞 𝐝𝐞𝐞𝐩! 🏊
𝐔𝐧𝐬𝐭𝐨𝐩𝐩𝐚𝐛𝐥𝐞! 💪

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🦅{LINE}🦅
   ☀️ {{user}} ☀️
   𝐑𝐎𝐘𝐀𝐋 𝐅𝐋𝐘!
🦅{LINE}🦅

𝐄𝐚𝐠𝐥𝐞 𝐡𝐚𝐬 𝐟𝐥𝐨𝐰𝐧! 🦅
𝐅𝐥𝐲 𝐡𝐢𝐠𝐡! 𝐃𝐫𝐞𝐚𝐦 𝐛𝐢𝐠! ☀️
𝐒𝐤𝐲 𝐢𝐬 𝐭𝐡𝐞 𝐥𝐢𝐦𝐢𝐭! 🌤️

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}"""
]

BAN_MSGS = [
    f"""⚖️{LINE}⚖️
   ⛔️ {{user}} ⛔️
   𝐉𝐔𝐒𝐓𝐈𝐂𝐄 𝐒𝐄𝐑𝐕𝐄𝐃!
⚖️{LINE}⚖️

𝐑𝐮𝐥𝐞𝐬 𝐰𝐞𝐫𝐞 𝐛𝐫𝐨𝐤𝐞𝐧! 🚨
𝐀𝐜𝐭𝐢𝐨𝐧 𝐰𝐚𝐬 𝐧𝐞𝐞𝐝𝐞𝐝! ⚡
𝐆𝐫𝐨𝐮𝐩 𝐢𝐬 𝐬𝐚𝐟𝐞! 🛡️

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🔨{LINE}🔨
   🚷 {{user}} 🚷
   𝐁𝐀𝐍 𝐇𝐀𝐌𝐌𝐄𝐑!
🔨{LINE}🔨

𝐎𝐮𝐭 𝐨𝐟 𝐠𝐚𝐦𝐞! ⚽
𝐍𝐨 𝐭𝐨𝐥𝐞𝐫𝐚𝐧𝐜𝐞! ❌
𝐑𝐮𝐥𝐞𝐬 𝐚𝐫𝐞 𝐫𝐮𝐥𝐞𝐬! 📜

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🚀{LINE}🚀
   💢 {{user}} 💢
   𝐄𝐉𝐄𝐂𝐓𝐄𝐃!
🚀{LINE}🚀

𝐘𝐨𝐮'𝐫𝐞 𝐨𝐮𝐭! 🌌
𝐆𝐫𝐨𝐮𝐩 𝐦𝐨𝐯𝐞𝐬 𝐨𝐧! 🚶
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🔒{LINE}🔒
   🚷 {{user}} 🚷
   𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 𝐋𝐎𝐂𝐊!
🔒{LINE}🔒

𝐀𝐜𝐜𝐞𝐬𝐬 𝐝𝐞𝐧𝐢𝐞𝐝! 🚫
𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝! 🛡️
𝐒𝐚𝐟𝐞 𝐬𝐩𝐚𝐜𝐞! ✨

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🚫{LINE}🚫
   ⛔️ {{user}} ⛔️
   𝐎𝐔𝐓𝐂𝐀𝐒𝐓!
🚫{LINE}🚫

𝐍𝐨 𝐦𝐨𝐫𝐞 𝐜𝐡𝐚𝐧𝐜𝐞𝐬! ❌
𝐖𝐚𝐫𝐧𝐢𝐧𝐠𝐬 𝐢𝐠𝐧𝐨𝐫𝐞𝐝! 👀
𝐓𝐢𝐦𝐞 𝐭𝐨 𝐠𝐨! 🚪

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""💀{LINE}💀
   ⚡ {{user}} ⚡
   𝐓𝐄𝐑𝐌𝐈𝐍𝐀𝐓𝐄𝐃!
💀{LINE}💀

𝐆𝐚𝐦𝐞 𝐨𝐯𝐞𝐫! 🎮
𝐍𝐨 𝐫𝐞𝐭𝐮𝐫𝐧! 🚫
𝐓𝐡𝐞 𝐞𝐧𝐝! 💥

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🗡️{LINE}🗡️
   💢 {{user}} 💢
   𝐁𝐀𝐍𝐈𝐒𝐇𝐄𝐃!
🗡️{LINE}🗡️

𝐅𝐨𝐫𝐞𝐯𝐞𝐫 𝐠𝐨𝐧𝐞! 🌅
𝐑𝐮𝐥𝐞𝐬 𝐰𝐞𝐫𝐞 𝐜𝐥𝐞𝐚𝐫! 📋
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🔐{LINE}🔐
   🚷 {{user}} 🚷
   𝐁𝐋𝐎𝐂𝐊𝐄𝐃!
🔐{LINE}🔐

𝐍𝐨 𝐞𝐧𝐭𝐫𝐲! 🚪
𝐏𝐞𝐫𝐦𝐚𝐧𝐞𝐧𝐭 𝐚𝐜𝐭𝐢𝐨𝐧! ⚖️
𝐌𝐨𝐯𝐞 𝐨𝐧! 🚶

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🎯{LINE}🎯
   ⛔️ {{user}} ⛔️
   𝐄𝐗𝐏𝐄𝐋𝐋𝐄𝐃!
🎯{LINE}🎯

𝐓𝐚𝐫𝐠𝐞𝐭 𝐫𝐞𝐦𝐨𝐯𝐞𝐝! 🎯
𝐍𝐨 𝐦𝐞𝐫𝐜𝐲! ❌
𝐑𝐮𝐥𝐞𝐬 𝐰𝐢𝐧! ⚔️

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""💥{LINE}💥
   💢 {{user}} 💢
   𝐔𝐋𝐓𝐈𝐌𝐀𝐓𝐄 𝐁𝐀𝐍!
💥{LINE}💥

𝐅𝐢𝐧𝐚𝐥 𝐬𝐭𝐫𝐢𝐤𝐞! ⚡
𝐍𝐨 𝐜𝐨𝐦𝐢𝐧𝐠 𝐛𝐚𝐜𝐤! 🚫
𝐈𝐭'𝐬 𝐨𝐯𝐞𝐫! 🎬

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}"""
]

LEFT_MSGS = [
    f"""👋{LINE}👋
   💔 {{user}} 💔
   𝐆𝐎𝐎𝐃𝐁𝐘𝐄!
👋{LINE}👋

𝐖𝐞'𝐥𝐥 𝐦𝐢𝐬𝐬 𝐲𝐨𝐮! 🥺
𝐓𝐚𝐤𝐞 𝐜𝐚𝐫𝐞! 🌈
𝐇𝐨𝐩𝐞 𝐭𝐨 𝐬𝐞𝐞 𝐚𝐠𝐚𝐢𝐧! 🌟

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🚶{LINE}🚶
   🌅 {{user}} 🌅
   𝐃𝐄𝐏𝐀𝐑𝐓𝐔𝐑𝐄!
🚶{LINE}🚶

𝐖𝐚𝐥𝐤𝐢𝐧𝐠 𝐚𝐰𝐚𝐲! 🚶
𝐓𝐡𝐞 𝐬𝐮𝐧 𝐬𝐞𝐭𝐬! 🌅
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🕊️{LINE}🕊️
   💫 {{user}} 💫
   𝐋𝐎𝐒𝐓 𝐒𝐎𝐔𝐋!
🕊️{LINE}🕊️

𝐅𝐥𝐲 𝐡𝐢𝐠𝐡! 🕊️
𝐅𝐢𝐧𝐝 𝐲𝐨𝐮𝐫 𝐰𝐚𝐲! 🌟
𝐘𝐨𝐮'𝐥𝐥 𝐛𝐞 𝐦𝐢𝐬𝐬𝐞𝐝! 💔

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🌊{LINE}🌊
   🚣 {{user}} 🚣
   𝐌𝐎𝐕𝐈𝐍𝐆 𝐎𝐍!
🌊{LINE}🌊

𝐒𝐚𝐢𝐥𝐢𝐧𝐠 𝐚𝐰𝐚𝐲! ⛵
𝐅𝐢𝐧𝐝 𝐩𝐞𝐚𝐜𝐞! 🌅
𝐓𝐡𝐞 𝐬𝐞𝐚 𝐰𝐚𝐢𝐭𝐬! 🌊

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""✌️{LINE}✌️
   ☮️ {{user}} ☮️
   𝐏𝐄𝐀𝐂𝐄 𝐎𝐔𝐓!
✌️{LINE}✌️

𝐒𝐩𝐫𝐞𝐚𝐝 𝐥𝐨𝐯𝐞! ❤️
𝐅𝐢𝐧𝐝 𝐣𝐨𝐲! 😊
𝐓𝐚𝐤𝐞 𝐜𝐚𝐫𝐞! ✌️

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🌹{LINE}🌹
   🥀 {{user}} 🥀
   𝐅𝐀𝐑𝐄𝐖𝐄𝐋𝐋!
🌹{LINE}🌹

𝐀 𝐫𝐨𝐬𝐞 𝐡𝐚𝐬 𝐟𝐚𝐥𝐥𝐞𝐧! 🌹
𝐋𝐞𝐠𝐞𝐧𝐝𝐬 𝐫𝐞𝐦𝐚𝐢𝐧! 📜
𝐒𝐞𝐞 𝐲𝐨𝐮 𝐬𝐨𝐨𝐧! 👋

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🌙{LINE}🌙
   🌟 {{user}} 🌟
   𝐌𝐎𝐎𝐍𝐋𝐈𝐆𝐇𝐓!
🌙{LINE}🌙

𝐌𝐨𝐨𝐧 𝐫𝐢𝐬𝐞𝐬! 🌙
𝐒𝐭𝐚𝐫 𝐟𝐚𝐥𝐥𝐬! 🌟
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 🌌

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""♾️{LINE}♾️
   🌈 {{user}} 🌈
   𝐄𝐍𝐃𝐋𝐄𝐒𝐒!
♾️{LINE}♾️

𝐉𝐨𝐮𝐫𝐧𝐞𝐲 𝐞𝐧𝐝𝐬! 🚶
𝐌𝐞𝐦𝐨𝐫𝐢𝐞𝐬 𝐥𝐚𝐬𝐭! 💫
𝐅𝐢𝐧𝐝 𝐲𝐨𝐮𝐫 𝐫𝐚𝐢𝐧𝐛𝐨𝐰! 🌈

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🦋{LINE}🦋
   🌺 {{user}} 🌺
   𝐁𝐔𝐓𝐓𝐄𝐑𝐅𝐋𝐘!
🦋{LINE}🦋

𝐒𝐩𝐫𝐞𝐚𝐝 𝐰𝐢𝐧𝐠𝐬! 🦋
𝐅𝐥𝐲 𝐟𝐫𝐞𝐞! 🌸
𝐅𝐢𝐧𝐝 𝐧𝐞𝐰 𝐠𝐚𝐫𝐝𝐞𝐧𝐬! 🌻

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""✨{LINE}✨
   ☄️ {{user}} ☄️
   𝐒𝐓𝐀𝐑𝐃𝐔𝐒𝐓!
✨{LINE}✨

𝐀 𝐬𝐭𝐚𝐫 𝐡𝐚𝐬 𝐠𝐨𝐧𝐞! 🌟
𝐒𝐡𝐢𝐧𝐞𝐬 𝐞𝐥𝐬𝐞𝐰𝐡𝐞𝐫𝐞! ✨
𝐆𝐨𝐨𝐝𝐛𝐲𝐞! 👋

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}"""
]

MUTE_MSGS = [
    f"""🔇{LINE}🔇
   🤐 {{user}} 🤐
   𝐌𝐔𝐓𝐄𝐃!
🔇{LINE}🔇

𝐔𝐬𝐞𝐫 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐦𝐮𝐭𝐞𝐝! 🤫
𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧: {{duration}} ⏱️
𝐁𝐲: {{admin}} 👑

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🔇{LINE}🔇
   ⛔️ {{user}} ⛔️
   𝐏𝐄𝐑𝐌𝐀𝐍𝐄𝐍𝐓 𝐌𝐔𝐓𝐄!
🔇{LINE}🔇

𝐏𝐞𝐫𝐦𝐚𝐧𝐞𝐧𝐭𝐥𝐲 𝐦𝐮𝐭𝐞𝐝! 🚫
𝐍𝐨 𝐭𝐨𝐥𝐞𝐫𝐚𝐧𝐜𝐞! ❌
𝐁𝐲: {{admin}} 👑

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}"""
]

UNMUTE_MSGS = [
    f"""🔊{LINE}🔊
   🗣️ {{user}} 🗣️
   𝐔𝐍𝐌𝐔𝐓𝐄𝐃!
🔊{LINE}🔊

𝐔𝐬𝐞𝐫 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐮𝐧𝐦𝐮𝐭𝐞𝐝! 🎉
𝐍𝐨𝐰 𝐭𝐡𝐞𝐲 𝐜𝐚𝐧 𝐬𝐩𝐞𝐚𝐤! 💬
𝐌𝐮𝐭𝐞 𝐢𝐬 𝐨𝐯𝐞𝐫! ⏰

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🔊{LINE}🔊
   🎉 {{user}} 🎉
   𝐌𝐔𝐓𝐄 𝐄𝐗𝐏𝐈𝐑𝐄𝐃!
🔊{LINE}🔊

𝐀𝐮𝐭𝐨-𝐮𝐧𝐦𝐮𝐭𝐞𝐝! 🤖
𝐓𝐢𝐦𝐞 𝐢𝐬 𝐮𝐩! ⏰
𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐛𝐚𝐜𝐤! 👋

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}"""
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

# ========== IS ADMIN ==========
async def is_admin(chat_id, user_id):
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except:
        return False

# ========== SEND NOTIFICATION ==========
async def send_notification(chat_id, user_mention, msg_template, extra=None):
    try:
        time = get_current_time()
        date = get_current_date()
        
        msg_text = msg_template.format(
            user=user_mention,
            time=time,
            date=date,
            **(extra or {})
        )
        
        emojis = ["🔥", "✨", "💎", "🌟", "🎉", "🚀", "👑", "💫"]
        footer = random.sample(emojis, 4)
        msg_text += f"\n\n{footer[0]} ᴘʀᴇᴍɪᴜᴍ {footer[1]} ᴜᴘᴅᴀᴛᴇ {footer[2]} ʙʏ {footer[3]} ʙᴏᴛ"
        
        video = get_random_video()
        if video and os.path.exists(video["path"]):
            await app.send_video(chat_id, video["path"], caption=msg_text, supports_streaming=True)
        else:
            await app.send_message(chat_id, msg_text)
    except Exception as e:
        logger.error(f"❌ Error: {e}")

# ========== GROUP AUTO-ADD ==========
@app.on_message(filters.group & filters.command("addgroup"))
async def add_group_from_group(client, message: Message):
    try:
        chat_id = message.chat.id
        chat_name = message.chat.title or f"Group {chat_id}"

        # 🔴 DELETE COMMAND MESSAGE INSTANTLY
        try:
            await message.delete()
        except:
            pass
        
        groups = load_groups()
        if str(chat_id) in groups:
            sent = await message.reply_text(
                f"""✅{LINE}✅
   ⚠️ **__𝗔𝗟𝗥𝗘𝗔𝗗𝗬 𝗔𝗗𝗗𝗘𝗗!__** ⚠️
✅{LINE}✅

📛 **__𝗡𝗔𝗠𝗘:__** `{chat_name}`
🆔 **__𝗜𝗗:__** `{chat_id}`
📅 **__𝗔𝗗𝗗𝗘𝗗:__** {groups[str(chat_id)]['added_at'][:16]}

🌟 **__𝗦𝗧𝗔𝗧𝗨𝗦:__** ✅ **__𝗔𝗖𝗧𝗜𝗩𝗘__**

{LINE}
🌌 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗔𝗖𝗧𝗜𝗩𝗘__** 🌌
{LINE}"""
            )
            await asyncio.sleep(5)
            try:
                await sent.delete()
            except:
                pass
            return
        
        save_group(chat_id, chat_name)
        
        confirm_text = f"""✅{LINE}✅
   🎯 **__𝗚𝗥𝗢𝗨𝗣 𝗔𝗗𝗗𝗘𝗗!__** 🎯
✅{LINE}✅

📛 **__𝗡𝗔𝗠𝗘:__** `{chat_name}`
🆔 **__𝗜𝗗:__** `{chat_id}`
📅 **__𝗗𝗔𝗧𝗘:__** {get_current_date()}
🕐 **__𝗧𝗜𝗠𝗘:__** {get_current_time()}

🌟 **__𝗦𝗧𝗔𝗧𝗨𝗦:__** ✅ **__𝗔𝗖𝗧𝗜𝗩𝗘__**

👤 **__𝗝𝗼𝗶𝗻__** │ 🚶 **__𝗟𝗲𝗮𝘃𝗲__** │ 🚫 **__𝗕𝗮𝗻__**

{LINE}
🌌 **__𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗘𝗡𝗔𝗕𝗟𝗘𝗗__** 🌌
{LINE}"""

        sent_msg = await message.reply_text(confirm_text)
        
        await asyncio.sleep(5)
        try:
            await sent_msg.delete()
        except:
            pass
        
        logger.info(f"✅ Group auto-added: {chat_name}")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")

# ========== SERVICE MESSAGES ==========
@app.on_message(filters.group & filters.service)
async def service_handler(client, message: Message):
    try:
        chat_id = message.chat.id
        if not is_group_enabled(chat_id):
            return
        
        if message.new_chat_members:
            for user in message.new_chat_members:
                if user.is_bot:
                    continue
                mention = f"[{user.first_name}](tg://user?id={user.id})"
                await send_notification(chat_id, mention, random.choice(JOIN_MSGS))
                logger.info(f"👤 JOIN: {user.first_name}")
        
        elif message.left_chat_member:
            user = message.left_chat_member
            if user.is_bot:
                return
            mention = f"[{user.first_name}](tg://user?id={user.id})"
            if hasattr(message, 'new_chat_members') and message.new_chat_members is None:
                await send_notification(chat_id, mention, random.choice(BAN_MSGS))
                logger.info(f"🚫 BANNED: {user.first_name}")
            else:
                await send_notification(chat_id, mention, random.choice(LEFT_MSGS))
                logger.info(f"🚶 LEFT: {user.first_name}")
                
    except Exception as e:
        logger.error(f"❌ Error: {e}")

# ========== MUTE COMMAND ==========
@app.on_message(filters.group & filters.command("tmkc"))
async def mute_user(client, message: Message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        # Check if user is admin or owner
        if not await is_admin(chat_id, user_id) and not is_owner(user_id):
            await message.reply_text(f"❌{LINE}❌\n   **__Only Admin & Owner Can Use!__**\n❌{LINE}❌")
            return
        
        if not message.reply_to_message:
            await message.reply_text(f"❌{LINE}❌\n   **__Reply to a user!__**\n❌{LINE}❌")
            return
        
        target = message.reply_to_message.from_user
        if target is None:
            await message.reply_text(f"❌{LINE}❌\n   **__User not found!__**\n❌{LINE}❌")
            return
        
        target_id = target.id
        
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply_text(f"❌{LINE}❌\n   **__/tmkc @user 1s/1m/1h/1d/1w/30d__**\n❌{LINE}❌")
            return
        
        time_str = parts[1]
        value, unit = parse_time(time_str)
        
        if value is None:
            await message.reply_text(f"❌{LINE}❌\n   **__Invalid time! Use 1s/1m/1h/1d/1w/30d__**\n❌{LINE}❌")
            return
        
        # Max limits
        if unit == "second" and value > 60:
            await message.reply_text(f"❌{LINE}❌\n   **__Max 60 seconds!__**\n❌{LINE}❌")
            return
        if unit == "minute" and value > 60:
            await message.reply_text(f"❌{LINE}❌\n   **__Max 60 minutes!__**\n❌{LINE}❌")
            return
        if unit == "day" and value > 30:
            await message.reply_text(f"❌{LINE}❌\n   **__Max 30 days!__**\n❌{LINE}❌")
            return
        if unit == "week" and value > 4:
            await message.reply_text(f"❌{LINE}❌\n   **__Max 4 weeks!__**\n❌{LINE}❌")
            return
        
        delta = timedelta(**{f"{unit}s": value})
        until_time = datetime.now() + delta
        until_str = until_time.isoformat()
        
        # Remove from revoke if exists
        remove_revoke(chat_id, target_id)
        
        save_mute(chat_id, target_id, until_str)
        
        try:
            await app.restrict_chat_member(
                chat_id=chat_id,
                user_id=target_id,
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False
                ),
                until_date=until_time
            )
        except Exception as e:
            await message.reply_text(f"❌ **__Error:__** {str(e)}")
            return
        
        admin_mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        user_mention = f"[{target.first_name}](tg://user?id={target_id})"
        duration = f"{value}{unit}"
        
        time = get_current_time()
        date = get_current_date()
        
        msg_text = MUTE_MSGS[0].format(
            user=user_mention,
            duration=duration,
            admin=admin_mention,
            time=time,
            date=date
        )
        
        emojis = ["🔇", "🤐", "⛔️"]
        msg_text += f"\n\n{emojis[0]} ᴍᴜᴛᴇ {emojis[1]} ᴀᴄᴛɪᴏɴ {emojis[2]}"
        
        video = get_random_video()
        if video and os.path.exists(video["path"]):
            await app.send_video(chat_id, video["path"], caption=msg_text, supports_streaming=True)
        else:
            await app.send_message(chat_id, msg_text)
        
        asyncio.create_task(auto_unmute(chat_id, target_id, target.first_name, until_time))
        logger.info(f"🔇 MUTED: {target.first_name} for {duration} by {message.from_user.first_name}")
        
    except Exception as e:
        logger.error(f"❌ Mute error: {e}")
        await message.reply_text(f"❌ **__Error:__** {str(e)}")

# ========== PERMANENT MUTE (OWNER ONLY) ==========
@app.on_message(filters.group & filters.command("revokemute"))
async def permanent_mute(client, message: Message):
    try:
        if not is_owner(message.from_user.id):
            await message.reply_text(f"❌{LINE}❌\n   **__This Command Only For Bot Father!__**\n❌{LINE}❌")
            return
        
        chat_id = message.chat.id
        
        if not message.reply_to_message:
            await message.reply_text(f"❌{LINE}❌\n   **__Reply to a user!__**\n❌{LINE}❌")
            return
        
        target = message.reply_to_message.from_user
        if target is None:
            await message.reply_text(f"❌{LINE}❌\n   **__User not found!__**\n❌{LINE}❌")
            return
        
        target_id = target.id
        
        # Remove from normal mute
        remove_mute(chat_id, target_id)
        
        # Save to revoke database
        save_revoke(chat_id, target_id)
        
        try:
            await app.restrict_chat_member(
                chat_id=chat_id,
                user_id=target_id,
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False
                ),
                until_date=datetime.now() + timedelta(days=365)
            )
        except Exception as e:
            await message.reply_text(f"❌ **__Error:__** {str(e)}")
            return
        
        admin_mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        user_mention = f"[{target.first_name}](tg://user?id={target_id})"
        
        time = get_current_time()
        date = get_current_date()
        
        msg_text = MUTE_MSGS[1].format(
            user=user_mention,
            admin=admin_mention,
            time=time,
            date=date
        )
        
        emojis = ["🔇", "⛔️", "🚫"]
        msg_text += f"\n\n{emojis[0]} ᴘᴇʀᴍᴀɴᴇɴᴛ {emojis[1]} ᴍᴜᴛᴇ {emojis[2]}"
        
        video = get_random_video()
        if video and os.path.exists(video["path"]):
            await app.send_video(chat_id, video["path"], caption=msg_text, supports_streaming=True)
        else:
            await app.send_message(chat_id, msg_text)
        
        logger.info(f"🔇 PERMANENT MUTE: {target.first_name} by {message.from_user.first_name}")
        
    except Exception as e:
        logger.error(f"❌ Permanent mute error: {e}")
        await message.reply_text(f"❌ **__Error:__** {str(e)}")

# ========== UNMUTE (OWNER ONLY) ==========
@app.on_message(filters.group & filters.command("unrevokemute"))
async def unmute_user(client, message: Message):
    try:
        if not is_owner(message.from_user.id):
            await message.reply_text(f"❌{LINE}❌\n   **__This Command Only For Bot Father!__**\n❌{LINE}❌")
            return
        
        chat_id = message.chat.id
        
        if not message.reply_to_message:
            await message.reply_text(f"❌{LINE}❌\n   **__Reply to a user!__**\n❌{LINE}❌")
            return
        
        target = message.reply_to_message.from_user
        if target is None:
            await message.reply_text(f"❌{LINE}❌\n   **__User not found!__**\n❌{LINE}❌")
            return
        
        target_id = target.id
        
        # Remove from revoke
        if not remove_revoke(chat_id, target_id):
            await message.reply_text(f"❌{LINE}❌\n   **__User is not permanently muted!__**\n❌{LINE}❌")
            return
        
        # Remove from normal mute too
        remove_mute(chat_id, target_id)
        
        try:
            await app.restrict_chat_member(
                chat_id=chat_id,
                user_id=target_id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True
                )
            )
        except:
            pass
        
        user_mention = f"[{target.first_name}](tg://user?id={target_id})"
        
        time = get_current_time()
        date = get_current_date()
        
        msg_text = UNMUTE_MSGS[0].format(
            user=user_mention,
            time=time,
            date=date
        )
        
        emojis = ["🔊", "🎉", "✅"]
        msg_text += f"\n\n{emojis[0]} ᴜɴᴍᴜᴛᴇ {emojis[1]} ᴀᴄᴛɪᴏɴ {emojis[2]}"
        
        video = get_random_video()
        if video and os.path.exists(video["path"]):
            await app.send_video(chat_id, video["path"], caption=msg_text, supports_streaming=True)
        else:
            await app.send_message(chat_id, msg_text)
        
        logger.info(f"🔊 UNMUTED: {target.first_name} by {message.from_user.first_name}")
        
    except Exception as e:
        logger.error(f"❌ Unmute error: {e}")
        await message.reply_text(f"❌ **__Error:__** {str(e)}")

# ========== AUTO UNMUTE ==========
async def auto_unmute(chat_id, user_id, user_name, until_time):
    try:
        now = datetime.now()
        wait_seconds = (until_time - now).total_seconds()
        
        if wait_seconds > 0:
            await asyncio.sleep(wait_seconds)
        
        # Check if not revoked
        if is_revoked(chat_id, user_id):
            return
        
        if is_muted(chat_id, user_id):
            remove_mute(chat_id, user_id)
            
            try:
                await app.restrict_chat_member(
                    chat_id=chat_id,
                    user_id=user_id,
                    permissions=ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True,
                        can_add_web_page_previews=True
                    )
                )
            except:
                pass
            
            user_mention = f"[{user_name}](tg://user?id={user_id})"
            time = get_current_time()
            date = get_current_date()
            
            msg_text = UNMUTE_MSGS[1].format(
                user=user_mention,
                time=time,
                date=date
            )
            
            emojis = ["🔊", "🤖", "✅"]
            msg_text += f"\n\n{emojis[0]} ᴀᴜᴛᴏ {emojis[1]} ᴜɴᴍᴜᴛᴇ {emojis[2]}"
            
            video = get_random_video()
            if video and os.path.exists(video["path"]):
                await app.send_video(chat_id, video["path"], caption=msg_text, supports_streaming=True)
            else:
                await app.send_message(chat_id, msg_text)
            
            logger.info(f"🔊 AUTO UNMUTED: {user_name}")
            
    except Exception as e:
        logger.error(f"❌ Auto unmute error: {e}")

# ========== DELETE REVOKED/MUTED USER MESSAGES ==========
@app.on_message(filters.group & filters.text)
async def delete_revoked_messages(client, message: Message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        # Check if user is revoked (permanent mute)
        if is_revoked(chat_id, user_id):
            await message.delete()
            logger.info(f"🗑️ Deleted message from revoked user: {message.from_user.first_name}")
            return
        
        # Check if user is muted
        if is_muted(chat_id, user_id):
            await message.delete()
            logger.info(f"🗑️ Deleted message from muted user: {message.from_user.first_name}")
            
    except Exception as e:
        logger.error(f"❌ Delete message error: {e}")

# ========== START COMMAND ==========
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    if not is_owner(message.from_user.id):
        await message.reply_text(
            f"""❌{LINE}❌
   ⛔️ **__𝗨𝗡𝗔𝗨𝗧𝗛𝗢𝗥𝗜𝗭𝗘𝗗!__** ⛔️
❌{LINE}❌

**__𝗛𝗲𝘆__** {message.from_user.first_name}! 👋

𝐓𝐡𝐢𝐬 𝐛𝐨𝐭 𝐢𝐬 𝐨𝐧𝐥𝐲 𝐟𝐨𝐫 𝐭𝐡𝐞 𝐨𝐰𝐧𝐞𝐫! 🚫
𝐏𝐥𝐞𝐚𝐬𝐞 𝐝𝐨𝐧'𝐭 𝐭𝐫𝐲 𝐭𝐨 𝐮𝐬𝐞! ❌

𝐈𝐟 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐚𝐝𝐝 𝐭𝐡𝐢𝐬 𝐛𝐨𝐭 𝐭𝐨 𝐲𝐨𝐮𝐫 𝐠𝐫𝐨𝐮𝐩, 📌
𝐂𝐨𝐧𝐭𝐚𝐜𝐭 **__𝐁𝐄𝐒𝐓 𝘾𝙃𝙀𝘼𝙏 ᵒʷⁿᵉʳ__** 💬

{LINE_BIG}
🕐 {get_current_time()}  •  📅 {get_current_date()}
{LINE_BIG}
🚫 **__𝗥𝗘𝗦𝗧𝗥𝗜𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗘𝗦𝗦__** 🚫
{LINE_BIG}""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📩 ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}")]
            ])
        )
        return
    
    await message.reply_text(
        f"""💎{LINE}💎
┏{LINE}┓
┃    💎 **__ᴘʀᴇᴍɪᴜᴍ ʙᴏᴛ__** 💎     
┗{LINE}┛
💎{LINE}💎

**__ʜᴇʏ__** {message.from_user.first_name}! 🌟  
**__ʙᴏᴛ ɪs ʀᴜɴɴɪɴɢ sᴍᴏᴏᴛʜʟʏ__** ✨

{LINE}
📹 **__ᴠɪᴅᴇᴏs:__** `{get_video_count()}`
👥 **__ɢʀᴏᴜᴘs:__** `{len(get_all_groups())}`
{LINE}

📹 **__/addvideo__** - **__ᴀᴅᴅ__**
📋 **__/videos__** - **__ᴠɪᴇᴡ__**
🗑️ **__/delvideo__** - **__ᴅᴇʟ__**
🧹 **__/clearvideos__** - **__ᴄʟᴇᴀʀ__**

➕ **__/addgroup__** - **__ᴀᴅᴅ__**
📋 **__/groups__** - **__ᴠɪᴇᴡ__**
❌ **__/delgroup__** - **__ʀᴇᴍ__**
🔄 **__/toggle__** - **__ᴛᴏɢɢʟᴇ__**

🔇 **__MUTE SYSTEM__**
• `/tmkc @user 1s/1m/1h/1d` - **__ᴛᴇᴍᴘ__**
• `/revokemute @user` - **__ᴘᴇʀᴍ__**
• `/unrevokemute @user` - **__ᴜɴᴍᴜᴛᴇ__**

📊 **__/stats__** - **__sᴛᴀᴛs__**

{LINE_BIG}
💎 **__ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴇ__** 💎
{LINE_BIG}"""
    )

# ========== OTHER COMMANDS ==========
@app.on_message(filters.command("addgroup") & filters.private)
async def add_group_private(client, message):
    if not is_owner(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply_text(f"❌{LINE}❌\n   **__/addgroup -100123456789__**\n❌{LINE}❌")
            return
        group_id = int(parts[1])
        group_name = parts[2] if len(parts) > 2 else f"Group {group_id}"
        save_group(group_id, group_name)
        await message.reply_text(f"✅ **__Group added!__**\n📛 {group_name}\n🆔 {group_id}")
    except Exception as e:
        await message.reply_text(f"❌ **__Error:__** {str(e)}")

@app.on_message(filters.command("groups") & filters.private)
async def groups_list(client, message):
    if not is_owner(message.from_user.id):
        return
    groups = get_all_groups()
    if not groups:
        await message.reply_text(f"❌{LINE}❌\n   **__No groups!__**\n❌{LINE}❌")
        return
    text = "👥 **__My Groups__**\n\n"
    for group_id, data in groups.items():
        status = "✅" if data.get("enabled", True) else "❌"
        text += f"{status} {data['name']}\n🆔 {group_id}\n\n"
    await message.reply_text(text)

@app.on_message(filters.command("delgroup") & filters.private)
async def delete_group(client, message):
    if not is_owner(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text(f"❌{LINE}❌\n   **__/delgroup -100123456789__**\n❌{LINE}❌")
            return
        group_id = int(parts[1])
        if remove_group(group_id):
            await message.reply_text("✅ **__Group removed!__**")
        else:
            await message.reply_text("❌ **__Not found!__**")
    except:
        await message.reply_text(f"❌{LINE}❌\n   **__Invalid!__**\n❌{LINE}❌")

@app.on_message(filters.command("toggle") & filters.private)
async def toggle_group(client, message):
    if not is_owner(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text(f"❌{LINE}❌\n   **__/toggle -100123456789__**\n❌{LINE}❌")
            return
        group_id = int(parts[1])
        status = toggle_group(group_id)
        await message.reply_text(f"✅ {group_id}\n📊 {'Enabled' if status else 'Disabled'}")
    except:
        await message.reply_text(f"❌{LINE}❌\n   **__Invalid!__**\n❌{LINE}❌")

@app.on_message(filters.command("addvideo") & filters.private)
async def add_video(client, message):
    if not is_owner(message.from_user.id):
        return
    status = await message.reply_text("⏳ **__Downloading...__**")
    try:
        if message.reply_to_message and message.reply_to_message.video:
            path = await message.reply_to_message.download()
            vid = save_video(path)
            await status.edit_text(f"✅ **__Video #{vid} saved!__**\n📹 Total: {get_video_count()}")
        else:
            await status.edit_text(f"❌{LINE}❌\n   **__Reply to a video!__**\n❌{LINE}❌")
    except Exception as e:
        await status.edit_text(f"❌ **__Error:__** {str(e)}")

@app.on_message(filters.command("videos") & filters.private)
async def list_videos(client, message):
    if not is_owner(message.from_user.id):
        return
    videos = load_videos()
    if not videos:
        await message.reply_text(f"❌{LINE}❌\n   **__No videos!__**\n❌{LINE}❌")
        return
    text = "🎬 **__Videos__**\n\n"
    for video in videos:
        used = "✅" if video.get("used", False) else "🔄"
        text += f"{used} #{video['id']} {video['name']}\n"
    text += f"\n📹 Total: {len(videos)}"
    await message.reply_text(text)

@app.on_message(filters.command("delvideo") & filters.private)
async def delete_video(client, message):
    if not is_owner(message.from_user.id):
        return
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text(f"❌{LINE}❌\n   **__/delvideo 1__**\n❌{LINE}❌")
            return
        vid = int(parts[1])
        if delete_video_by_id(vid):
            await message.reply_text(f"✅ **__Video #{vid} deleted!__**")
        else:
            await message.reply_text(f"❌{LINE}❌\n   **__Not found!__**\n❌{LINE}❌")
    except:
        await message.reply_text(f"❌{LINE}❌\n   **__Invalid!__**\n❌{LINE}❌")

@app.on_message(filters.command("clearvideos") & filters.private)
async def clear_videos(client, message):
    if not is_owner(message.from_user.id):
        return
    videos = load_videos()
    if not videos:
        await message.reply_text(f"❌{LINE}❌\n   **__No videos!__**\n❌{LINE}❌")
        return
    for video in videos:
        if os.path.exists(video["path"]):
            os.remove(video["path"])
    with open(VIDEO_DB, "w") as f:
        json.dump([], f)
    await message.reply_text(f"🗑️ **__{len(videos)} cleared!__**")

@app.on_message(filters.command("stats") & filters.private)
async def stats_cmd(client, message):
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
    text = f"""📊 **__Stats__**

📹 Videos: {len(videos)}
🔄 Unused: {len(videos) - used}
✅ Used: {used}
💾 Size: {total_size / (1024*1024):.2f} MB

👥 Groups: {len(groups)}
✅ Enabled: {sum(1 for g in groups.values() if g.get('enabled', True))}

⏰ {datetime.now(IST).strftime('%d %b %Y %I:%M %p')}
{LINE_BIG}
💎 Premium Active 💎
{LINE_BIG}"""
    await message.reply_text(text)

# ========== RUN ==========
if __name__ == "__main__":
    print("\n" + "="*40)
    print("🚀 PREMIUM BOT STARTING...")
    print("🔇 MUTE SYSTEM ACTIVE")
    print("="*40 + "\n")
    
    for db in [VIDEO_DB, GROUPS_DB, MUTE_DB, REVOKE_DB]:
        if not os.path.exists(db):
            with open(db, "w") as f:
                json.dump({} if db != VIDEO_DB else [], f)
    
    os.makedirs("downloads", exist_ok=True)
    
    print(f"📹 Videos: {get_video_count()}")
    print(f"👥 Groups: {len(get_all_groups())}")
    print("\n" + "="*40)
    print("🤖 BOT IS RUNNING!")
    print("🔇 MUTE SYSTEM ACTIVE!")
    print("="*40 + "\n")
    
    try:
        app.run()
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
