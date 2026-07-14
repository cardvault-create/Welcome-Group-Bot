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
BOT_TOKEN = "8603632286:AAHZ0y_rJ7UTZ6jRWCSvej0JjUhVtuiTRpY"
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
LINE = "━━━━━━━━━━━━━━━━━━━"
LINE_BIG = "━━━━━━━━━━━━━━━━━━━━━━"

# ========== USED VIDEOS TRACKING ==========
used_video_ids = []

# ========== ERROR MESSAGES WITH BUTTON ==========
def get_owner_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(" ✾ ☆ .•°Contact-Father°˳˳˳!!♡🇵🇹", url=f"https://t.me/{OWNER_USERNAME}")]
    ])

OWNER_ERROR_MSG = f"""❌{LINE}❌
  ☆ 
  .•° <b>Hey! You can't use this command!</b> ❗
  ✾ <b>This User Is A Bot Father, You Can't Do Anything!</b> °˳˳˳!!♡🇵🇹
❌{LINE}❌"""

ADMIN_ERROR_MSG = f"""❌{LINE}❌
  ☆ 
  .•° <b>Hey! You can't use this command!</b> ❗
  ✾ <b>This User Is A Group Admin, You Can't Do Anything!</b> °˳˳˳!!♡🇵🇹
❌{LINE}❌"""

USER_ERROR_MSG = f"""❌{LINE}❌
  ☆ 
  .•° <b>Hey! You can't use this command!</b> ❗
  ✾ <b>You are not a group admin, You can't do Anything!</b> °˳˳˳!!♡🇵🇹
❌{LINE}❌"""

UNAUTHORIZED_MSG = f"""❌{LINE}❌
   ⛔️ <b>UNAUTHORIZED!</b> ⛔️
❌{LINE}❌

<b>Hey</b> {{user}}! 👋

<b>This bot is only for the owner!</b> 🚫
<b>Please don't try to use!</b> ❌

<b>If you want to add this bot to your group,</b> 📌
<b>Contact</b> <b>BEST CHEAT OWNER</b> 💬

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}
🚫 <b>RESTRICTED ACCESS</b> 🚫
{LINE_BIG}"""

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
    global used_video_ids
    
    videos = load_videos()
    if not videos:
        return None
    
    available = [v for v in videos if v["id"] not in used_video_ids]
    
    if not available:
        used_video_ids.clear()
        available = videos
    
    video = random.choice(available)
    used_video_ids.append(video["id"])
    
    if len(used_video_ids) > 20:
        used_video_ids = used_video_ids[-10:]
    
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
            if video_id in used_video_ids:
                used_video_ids.remove(video_id)
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

def get_mute_until(group_id, user_id):
    mutes = load_mutes()
    key = f"{group_id}_{user_id}"
    if key in mutes:
        return mutes[key]
    return None

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

def get_revoked_users(group_id):
    revoke = load_revoke()
    users = []
    for key in revoke:
        try:
            g_id, u_id = key.split("_")
            if int(g_id) == group_id:
                users.append(int(u_id))
        except:
            pass
    return users

# ========== TIME FUNCTIONS ==========
def get_current_time():
    return datetime.now(IST).strftime("%I:%M:%S %p")

def get_current_date():
    return datetime.now(IST).strftime("%B %d, %Y")

def get_unmute_time(until_str):
    try:
        until_time = datetime.fromisoformat(until_str)
        until_time_ist = until_time.astimezone(IST)
        return until_time_ist.strftime("%I:%M:%S %p")
    except:
        return "Permanent"

def parse_time(time_str):
    if time_str.endswith('s'):
        val = int(time_str[:-1])
        if 30 <= val <= 60:
            return val, "second"
    elif time_str.endswith('m'):
        val = int(time_str[:-1])
        if 1 <= val <= 60:
            return val, "minute"
    elif time_str.endswith('h'):
        val = int(time_str[:-1])
        if 1 <= val <= 24:
            return val, "hour"
    elif time_str.endswith('d'):
        val = int(time_str[:-1])
        if 1 <= val <= 30:
            return val, "day"
    elif time_str.endswith('w'):
        val = int(time_str[:-1])
        if 1 <= val <= 3:
            return val, "week"
    return None, None

def format_duration(value, unit):
    if unit == "second":
        return f"{value} second{'s' if value > 1 else ''}"
    elif unit == "minute":
        return f"{value} minute{'s' if value > 1 else ''}"
    elif unit == "hour":
        return f"{value} hour{'s' if value > 1 else ''}"
    elif unit == "day":
        return f"{value} day{'s' if value > 1 else ''}"
    elif unit == "week":
        return f"{value} week{'s' if value > 1 else ''}"
    return f"{value}{unit}"

# ========== SHORT MESSAGES ==========
JOIN_MSGS = [
    f"""🔥{LINE}🔥
   🐦‍🔥 {{user}} 🐦‍🔥
   **__𝐏𝐇𝐎𝐄𝐍𝐈𝐗 𝐑𝐈𝐒𝐄𝐒!__**
🔥{LINE}🔥

**__𝐑𝐢𝐬𝐢𝐧𝐠 𝐟𝐫𝐨𝐦 𝐚𝐬𝐡!__** 🔥
**__𝐘𝐨𝐮'𝐫𝐞 𝐮𝐧𝐬𝐭𝐨𝐩𝐩𝐚𝐛𝐥𝐞!__** 💪
**__𝐁𝐨𝐫𝐧 𝐭𝐨 𝐰𝐢𝐧!__** 🏆

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""👑{LINE}👑
   🦁 {{user}} 🦁
   **__𝐊𝐈𝐍𝐆 𝐖𝐄𝐋𝐂𝐎𝐌𝐄!__**
👑{LINE}👑

**__𝐓𝐡𝐞 𝐤𝐢𝐧𝐠 𝐢𝐬 𝐡𝐞𝐫𝐞!__** 👑
**__𝐘𝐨𝐮'𝐫𝐞 𝐭𝐡𝐞 𝐫𝐮𝐥𝐞𝐫!__** ⚔️
**__𝐋𝐞𝐭'𝐬 𝐜𝐨𝐧𝐪𝐮𝐞𝐫!__** 🏰

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🐉{LINE}🐉
   ⚡ {{user}} ⚡
   **__𝐃𝐑𝐀𝐆𝐎𝐍 𝐀𝐑𝐑𝐈𝐕𝐄𝐃!__**
🐉{LINE}🐉

**__𝐓𝐡𝐞 𝐝𝐫𝐚𝐠𝐨𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞!__** 🐲
**__𝐅𝐢𝐫𝐞 𝐢𝐧 𝐭𝐡𝐞 𝐬𝐨𝐮𝐥!__** 🔥
**__𝐔𝐧𝐥𝐞𝐚𝐬𝐡 𝐩𝐨𝐰𝐞𝐫!__** ⚡

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🐺{LINE}🐺
   🌙 {{user}} 🌙
   **__𝐋𝐄𝐆𝐄𝐍𝐃 𝐉𝐎𝐈𝐍𝐒!__**
🐺{LINE}🐺

**__𝐖𝐨𝐥𝐟 𝐡𝐚𝐬 𝐚𝐫𝐫𝐢𝐯𝐞𝐝!__** 🌕
**__𝐋𝐞𝐚𝐝𝐞𝐫 𝐨𝐟 𝐩𝐚𝐜𝐤!__** 🐾
**__𝐋𝐞𝐭'𝐬 𝐡𝐨𝐰𝐥!__** 🌙

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""💪{LINE}💪
   🦍 {{user}} 🦍
   **__𝐓𝐈𝐓𝐀𝐍 𝐀𝐑𝐑𝐈𝐕𝐄𝐃!__**
💪{LINE}💪

**__𝐓𝐢𝐭𝐚𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞!__** 🏔️
**__𝐒𝐭𝐫𝐞𝐧𝐠𝐭𝐡 𝐮𝐧𝐥𝐞𝐚𝐬𝐡!__** ⚡
**__𝐋𝐞𝐭'𝐬 𝐝𝐨𝐦𝐢𝐧𝐚𝐭𝐞!__** 🔥

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🌌{LINE}🌌
   🚀 {{user}} 🚀
   **__𝐆𝐀𝐋𝐀𝐗𝐘 𝐉𝐎𝐈𝐍!__**
🌌{LINE}🌌

**__𝐀 𝐬𝐭𝐚𝐫 𝐢𝐬 𝐛𝐨𝐫𝐧!__** 🌟
**__𝐁𝐞𝐲𝐨𝐧𝐝 𝐭𝐡𝐢𝐬 𝐰𝐨𝐫𝐥𝐝!__** 👽
**__𝐂𝐨𝐬𝐦𝐨𝐬 𝐰𝐚𝐢𝐭𝐬!__** 🌠

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🏯{LINE}🏯
   🐯 {{user}} 🐯
   **__𝐄𝐌𝐏𝐄𝐑𝐎𝐑 𝐖𝐄𝐋𝐂𝐎𝐌𝐄!__**
🏯{LINE}🏯

**__𝐄𝐦𝐩𝐞𝐫𝐨𝐫 𝐚𝐫𝐫𝐢𝐯𝐞𝐝!__** 👑
**__𝐑𝐞𝐬𝐩𝐞𝐜𝐭 𝐭𝐡𝐞 𝐜𝐫𝐨𝐰𝐧!__** ⚜️
**__𝐋𝐞𝐠𝐞𝐧𝐝 𝐛𝐞𝐠𝐢𝐧𝐬!__** 📜

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🦄{LINE}🦄
   ✨ {{user}} ✨
   **__𝐌𝐀𝐆𝐈𝐂 𝐉𝐎𝐈𝐍!__**
🦄{LINE}🦄

**__𝐔𝐧𝐢𝐜𝐨𝐫𝐧 𝐢𝐬 𝐡𝐞𝐫𝐞!__** 🦄
**__𝐌𝐚𝐠𝐢𝐜 𝐢𝐧 𝐚𝐢𝐫!__** ✨
**__𝐎𝐧𝐞 𝐨𝐟 𝐚 𝐤𝐢𝐧𝐝!__** 💫

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🦈{LINE}🦈
   ⚓ {{user}} ⚓
   **__𝐄𝐋𝐈𝐓𝐄 𝐀𝐑𝐑𝐈𝐕𝐄𝐃!__**
🦈{LINE}🦈

**__𝐒𝐡𝐚𝐫𝐤 𝐢𝐬 𝐡𝐞𝐫𝐞!__** 🌊
**__𝐑𝐮𝐥𝐞 𝐭𝐡𝐞 𝐝𝐞𝐞𝐩!__** 🏊
**__𝐔𝐧𝐬𝐭𝐨𝐩𝐩𝐚𝐛𝐥𝐞!__** 💪

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🦅{LINE}🦅
   ☀️ {{user}} ☀️
   **__𝐑𝐎𝐘𝐀𝐋 𝐅𝐋𝐘!__**
🦅{LINE}🦅

**__𝐄𝐚𝐠𝐥𝐞 𝐡𝐚𝐬 𝐟𝐥𝐨𝐰𝐧!__** 🦅
**__𝐅𝐥𝐲 𝐡𝐢𝐠𝐡! 𝐃𝐫𝐞𝐚𝐦 𝐛𝐢𝐠!__** ☀️
**__𝐒𝐤𝐲 𝐢𝐬 𝐭𝐡𝐞 𝐥𝐢𝐦𝐢𝐭!__** 🌤️

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}"""
]

BAN_MSGS = [
    f"""⚖️{LINE}⚖️
   ⛔️ {{user}} ⛔️
   **__𝐉𝐔𝐒𝐓𝐈𝐂𝐄 𝐒𝐄𝐑𝐕𝐄𝐃!__**
⚖️{LINE}⚖️

**__𝐑𝐮𝐥𝐞𝐬 𝐰𝐞𝐫𝐞 𝐛𝐫𝐨𝐤𝐞𝐧!__** 🚨
**__𝐀𝐜𝐭𝐢𝐨𝐧 𝐰𝐚𝐬 𝐧𝐞𝐞𝐝𝐞𝐝!__** ⚡
**__𝐆𝐫𝐨𝐮𝐩 𝐢𝐬 𝐬𝐚𝐟𝐞!__** 🛡️

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🔨{LINE}🔨
   🚷 {{user}} 🚷
   **__𝐁𝐀𝐍 𝐇𝐀𝐌𝐌𝐄𝐑!__**
🔨{LINE}🔨

**__𝐎𝐮𝐭 𝐨𝐟 𝐠𝐚𝐦𝐞!__** ⚽
**__𝐍𝐨 𝐭𝐨𝐥𝐞𝐫𝐚𝐧𝐜𝐞!__** ❌
**__𝐑𝐮𝐥𝐞𝐬 𝐚𝐫𝐞 𝐫𝐮𝐥𝐞𝐬!__** 📜

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🚀{LINE}🚀
   💢 {{user}} 💢
   **__𝐄𝐉𝐄𝐂𝐓𝐄𝐃!__**
🚀{LINE}🚀

**__𝐘𝐨𝐮'𝐫𝐞 𝐨𝐮𝐭!__** 🌌
**__𝐆𝐫𝐨𝐮𝐩 𝐦𝐨𝐯𝐞𝐬 𝐨𝐧!__** 🚶
**__𝐆𝐨𝐨𝐝𝐛𝐲𝐞!__** 👋

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🔒{LINE}🔒
   🚷 {{user}} 🚷
   **__𝐒𝐄𝐂𝐔𝐑𝐈𝐓𝐘 𝐋𝐎𝐂𝐊!__**
🔒{LINE}🔒

**__𝐀𝐜𝐜𝐞𝐬𝐬 𝐝𝐞𝐧𝐢𝐞𝐝!__** 🚫
**__𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐚𝐜𝐭𝐢𝐯𝐚𝐭𝐞𝐝!__** 🛡️
**__𝐒𝐚𝐟𝐞 𝐬𝐩𝐚𝐜𝐞!__** ✨

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🚫{LINE}🚫
   ⛔️ {{user}} ⛔️
   **__𝐎𝐔𝐓𝐂𝐀𝐒𝐓!__**
🚫{LINE}🚫

**__𝐍𝐨 𝐦𝐨𝐫𝐞 𝐜𝐡𝐚𝐧𝐜𝐞𝐬!__** ❌
**__𝐖𝐚𝐫𝐧𝐢𝐧𝐠𝐬 𝐢𝐠𝐧𝐨𝐫𝐞𝐝!__** 👀
**__𝐓𝐢𝐦𝐞 𝐭𝐨 𝐠𝐨!__** 🚪

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""💀{LINE}💀
   ⚡ {{user}} ⚡
   **__𝐓𝐄𝐑𝐌𝐈𝐍𝐀𝐓𝐄𝐃!__**
💀{LINE}💀

**__𝐆𝐚𝐦𝐞 𝐨𝐯𝐞𝐫!__** 🎮
**__𝐍𝐨 𝐫𝐞𝐭𝐮𝐫𝐧!__** 🚫
**__𝐓𝐡𝐞 𝐞𝐧𝐝!__** 💥

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🗡️{LINE}🗡️
   💢 {{user}} 💢
   **__𝐁𝐀𝐍𝐈𝐒𝐇𝐄𝐃!__**
🗡️{LINE}🗡️

**__𝐅𝐨𝐫𝐞𝐯𝐞𝐫 𝐠𝐨𝐧𝐞!__** 🌅
**__𝐑𝐮𝐥𝐞𝐬 𝐰𝐞𝐫𝐞 𝐜𝐥𝐞𝐚𝐫!__** 📋
**__𝐆𝐨𝐨𝐝𝐛𝐲𝐞!__** 👋

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🔐{LINE}🔐
   🚷 {{user}} 🚷
   **__𝐁𝐋𝐎𝐂𝐊𝐄𝐃!__**
🔐{LINE}🔐

**__𝐍𝐨 𝐞𝐧𝐭𝐫𝐲!__** 🚪
**__𝐏𝐞𝐫𝐦𝐚𝐧𝐞𝐧𝐭 𝐚𝐜𝐭𝐢𝐨𝐧!__** ⚖️
**__𝐌𝐨𝐯𝐞 𝐨𝐧!__** 🚶

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🎯{LINE}🎯
   ⛔️ {{user}} ⛔️
   **__𝐄𝐗𝐏𝐄𝐋𝐋𝐄𝐃!__**
🎯{LINE}🎯

**__𝐓𝐚𝐫𝐠𝐞𝐭 𝐫𝐞𝐦𝐨𝐯𝐞𝐝!__** 🎯
**__𝐍𝐨 𝐦𝐞𝐫𝐜𝐲!__** ❌
**__𝐑𝐮𝐥𝐞𝐬 𝐰𝐢𝐧!__** ⚔️

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""💥{LINE}💥
   💢 {{user}} 💢
   **__𝐔𝐋𝐓𝐈𝐌𝐀𝐓𝐄 𝐁𝐀𝐍!__**
💥{LINE}💥

**__𝐅𝐢𝐧𝐚𝐥 𝐬𝐭𝐫𝐢𝐤𝐞!__** ⚡
**__𝐍𝐨 𝐜𝐨𝐦𝐢𝐧𝐠 𝐛𝐚𝐜𝐤!__** 🚫
**__𝐈𝐭'𝐬 𝐨𝐯𝐞𝐫!__** 🎬

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}"""
]

LEFT_MSGS = [
    f"""👋{LINE}👋
   💔 {{user}} 💔
   **__𝐆𝐎𝐎𝐃𝐁𝐘𝐄!__**
👋{LINE}👋

**__𝐖𝐞'𝐥𝐥 𝐦𝐢𝐬𝐬 𝐲𝐨𝐮!__** 🥺
**__𝐓𝐚𝐤𝐞 𝐜𝐚𝐫𝐞!__** 🌈
**__𝐇𝐨𝐩𝐞 𝐭𝐨 𝐬𝐞𝐞 𝐚𝐠𝐚𝐢𝐧!__** 🌟

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🚶{LINE}🚶
   🌅 {{user}} 🌅
   **__𝐃𝐄𝐏𝐀𝐑𝐓𝐔𝐑𝐄!__**
🚶{LINE}🚶

**__𝐖𝐚𝐥𝐤𝐢𝐧𝐠 𝐚𝐰𝐚𝐲!__** 🚶
**__𝐓𝐡𝐞 𝐬𝐮𝐧 𝐬𝐞𝐭𝐬!__** 🌅
**__𝐆𝐨𝐨𝐝𝐛𝐲𝐞!__** 👋

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🕊️{LINE}🕊️
   💫 {{user}} 💫
   **__𝐋𝐎𝐒𝐓 𝐒𝐎𝐔𝐋!__**
🕊️{LINE}🕊️

**__𝐅𝐥𝐲 𝐡𝐢𝐠𝐡!__** 🕊️
**__𝐅𝐢𝐧𝐝 𝐲𝐨𝐮𝐫 𝐰𝐚𝐲!__** 🌟
**__𝐘𝐨𝐮'𝐥𝐥 𝐛𝐞 𝐦𝐢𝐬𝐬𝐞𝐝!__** 💔

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🌊{LINE}🌊
   🚣 {{user}} 🚣
   **__𝐌𝐎𝐕𝐈𝐍𝐆 𝐎𝐍!__**
🌊{LINE}🌊

**__𝐒𝐚𝐢𝐥𝐢𝐧𝐠 𝐚𝐰𝐚𝐲!__** ⛵
**__𝐅𝐢𝐧𝐝 𝐩𝐞𝐚𝐜𝐞!__** 🌅
**__𝐓𝐡𝐞 𝐬𝐞𝐚 𝐰𝐚𝐢𝐭𝐬!__** 🌊

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""✌️{LINE}✌️
   ☮️ {{user}} ☮️
   **__𝐏𝐄𝐀𝐂𝐄 𝐎𝐔𝐓!__**
✌️{LINE}✌️

**__𝐒𝐩𝐫𝐞𝐚𝐝 𝐥𝐨𝐯𝐞!__** ❤️
**__𝐅𝐢𝐧𝐝 𝐣𝐨𝐲!__** 😊
**__𝐓𝐚𝐤𝐞 𝐜𝐚𝐫𝐞!__** ✌️

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🌹{LINE}🌹
   🥀 {{user}} 🥀
   **__𝐅𝐀𝐑𝐄𝐖𝐄𝐋𝐋!__**
🌹{LINE}🌹

**__𝐀 𝐫𝐨𝐬𝐞 𝐡𝐚𝐬 𝐟𝐚𝐥𝐥𝐞𝐧!__** 🌹
**__𝐋𝐞𝐠𝐞𝐧𝐝𝐬 𝐫𝐞𝐦𝐚𝐢𝐧!__** 📜
**__𝐒𝐞𝐞 𝐲𝐨𝐮 𝐬𝐨𝐨𝐧!__** 👋

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🌙{LINE}🌙
   🌟 {{user}} 🌟
   **__𝐌𝐎𝐎𝐍𝐋𝐈𝐆𝐇𝐓!__**
🌙{LINE}🌙

**__𝐌𝐨𝐨𝐧 𝐫𝐢𝐬𝐞𝐬!__** 🌙
**__𝐒𝐭𝐚𝐫 𝐟𝐚𝐥𝐥𝐬!__** 🌟
**__𝐆𝐨𝐨𝐝𝐛𝐲𝐞!__** 🌌

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""♾️{LINE}♾️
   🌈 {{user}} 🌈
   **__𝐄𝐍𝐃𝐋𝐄𝐒𝐒!__**
♾️{LINE}♾️

**__𝐉𝐨𝐮𝐫𝐧𝐞𝐲 𝐞𝐧𝐝𝐬!__** 🚶
**__𝐌𝐞𝐦𝐨𝐫𝐢𝐞𝐬 𝐥𝐚𝐬𝐭!__** 💫
**__𝐅𝐢𝐧𝐝 𝐲𝐨𝐮𝐫 𝐫𝐚𝐢𝐧𝐛𝐨𝐰!__** 🌈

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🦋{LINE}🦋
   🌺 {{user}} 🌺
   **__𝐁𝐔𝐓𝐓𝐄𝐑𝐅𝐋𝐘!__**
🦋{LINE}🦋

**__𝐒𝐩𝐫𝐞𝐚𝐝 𝐰𝐢𝐧𝐠𝐬!__** 🦋
**__𝐅𝐥𝐲 𝐟𝐫𝐞𝐞!__** 🌸
**__𝐅𝐢𝐧𝐝 𝐧𝐞𝐰 𝐠𝐚𝐫𝐝𝐞𝐧𝐬!__** 🌻

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""✨{LINE}✨
   ☄️ {{user}} ☄️
   **__𝐒𝐓𝐀𝐑𝐃𝐔𝐒𝐓!__**
✨{LINE}✨

**__𝐀 𝐬𝐭𝐚𝐫 𝐡𝐚𝐬 𝐠𝐨𝐧𝐞!__** 🌟
**__𝐒𝐡𝐢𝐧𝐞𝐬 𝐞𝐥𝐬𝐞𝐰𝐡𝐞𝐫𝐞!__** ✨
**__𝐆𝐨𝐨𝐝𝐛𝐲𝐞!__** 👋

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}"""
]

MUTE_MSGS = [
    f"""🔇{LINE}🔇
   🤐 {{user}} 🤐
   **__𝐌𝐔𝐓𝐄𝐃!__**
🔇{LINE}🔇

**__𝐔𝐬𝐞𝐫 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐦𝐮𝐭𝐞𝐝!__** 🤫
**__𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧:__** {{duration}} ⏱️
**__𝐔𝐧𝐦𝐮𝐭𝐞 𝐚𝐭:__** {{unmute_time}} 🕐
**__𝐁𝐲:__** {{admin}} 👑

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🔊{LINE}🔊
   🗣️ {{user}} 🗣️
   **__𝐔𝐍𝐌𝐔𝐓𝐄𝐃!__**
🔊{LINE}🔊

**__𝐔𝐬𝐞𝐫 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐮𝐧𝐦𝐮𝐭𝐞𝐝!__** 🎉
**__𝐍𝐨𝐰 𝐭𝐡𝐞𝐲 𝐜𝐚𝐧 𝐬𝐩𝐞𝐚𝐤!__** 💬
**__𝐌𝐮𝐭𝐞 𝐢𝐬 𝐨𝐯𝐞𝐫!__** ⏰

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🔊{LINE}🔊
   🎉 {{user}} 🎉
   **__𝐌𝐔𝐓𝐄 𝐄𝐗𝐏𝐈𝐑𝐄𝐃!__**
🔊{LINE}🔊

**__𝐀𝐮𝐭𝐨-𝐮𝐧𝐦𝐮𝐭𝐞𝐝!__** 🤖
**__𝐓𝐢𝐦𝐞 𝐢𝐬 𝐮𝐩!__** ⏰
**__𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐛𝐚𝐜𝐤!__** 👋

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}"""
]

REVOKE_MSGS = [
    f"""🔇{LINE}🔇
   🚫 {{user}} 🚫
   **__𝐑𝐄𝐕𝐎𝐊𝐄𝐃!__**
🔇{LINE}🔇

**__𝐔𝐬𝐞𝐫'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬 𝐰𝐢𝐥𝐥 𝐛𝐞 𝐝𝐞𝐥𝐞𝐭𝐞𝐝!__** 🗑️
**__𝐀𝐥𝐥 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬 𝐰𝐢𝐥𝐥 𝐛𝐞 𝐚𝐮𝐭𝐨-𝐝𝐞𝐥𝐞𝐭𝐞𝐝!__** 🤖
**__𝐁𝐲:__** {{admin}} 👑

{LINE_BIG}
🕐 {{time}}  •  📅 {{date}}
{LINE_BIG}""",

    f"""🔊{LINE}🔊
   ✅ {{user}} ✅
   **__𝐔𝐍𝐑𝐄𝐕𝐎𝐊𝐄𝐃!__**
🔊{LINE}🔊

**__𝐔𝐬𝐞𝐫'𝐬 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬 𝐰𝐢𝐥𝐥 𝐧𝐨𝐭 𝐛𝐞 𝐝𝐞𝐥𝐞𝐭𝐞𝐝!__** 🎉
**__𝐍𝐨𝐰 𝐭𝐡𝐞𝐲 𝐜𝐚𝐧 𝐬𝐞𝐧𝐝 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬 𝐧𝐨𝐫𝐦𝐚𝐥𝐥𝐲!__** 💬
**__𝐁𝐲:__** {{admin}} 👑

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

# ========== 🔴 FIXED: IS ADMIN OR CREATOR ==========
async def is_admin_or_creator(chat_id, user_id):
    try:
        member = await app.get_chat_member(chat_id, user_id)
        logger.info(f"🔍 User {user_id} status: {member.status}")
        return member.status in ["administrator", "creator"]
    except Exception as e:
        logger.error(f"❌ Admin check error: {e}")
        return False

# ========== CHECK IF USER IN GROUP ==========
async def is_user_in_group(chat_id, user_id):
    try:
        member = await app.get_chat_member(chat_id, user_id)
        return member is not None
    except:
        return False

# ========== GET USER FROM ID OR USERNAME ==========
async def get_user_from_input(client, input_str, chat_id):
    try:
        if input_str.isdigit():
            user_id = int(input_str)
            try:
                user = await client.get_users(user_id)
                return user
            except:
                try:
                    member = await client.get_chat_member(chat_id, user_id)
                    return member.user
                except:
                    return None
        else:
            username = input_str.replace("@", "")
            try:
                user = await client.get_users(username)
                return user
            except:
                return None
    except:
        return None

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
        
        msg_text += f"\n\n✨ ᴘʀᴇᴍɪᴜᴍ 💎 ᴜᴘᴅᴀᴛᴇ 👑 ʙʏ 💫 ʙᴏᴛ"
        
        video = get_random_video()
        if video and os.path.exists(video["path"]):
            await app.send_video(chat_id, video["path"], caption=msg_text, supports_streaming=True)
        else:
            await app.send_message(chat_id, msg_text)
    except Exception as e:
        logger.error(f"❌ Error in send_notification: {e}")

# ========== GROUP AUTO-ADD ==========
@app.on_message(filters.group & filters.command("addgroup"))
async def add_group_from_group(client, message: Message):
    try:
        chat_id = message.chat.id
        chat_name = message.chat.title or f"Group {chat_id}"

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
        logger.error(f"❌ Error in addgroup: {e}")

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
        logger.error(f"❌ Error in service_handler: {e}")

# ========== 🔴 MUTE COMMAND (ADMIN + CREATOR + OWNER) ==========
@app.on_message(filters.group & filters.command("tmkc"))
async def mute_user(client, message: Message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        # Check if user is revoked - delete command silently
        if is_revoked(chat_id, user_id):
            try:
                await message.delete()
            except:
                pass
            return
        
        # 🔴 FIX: Check if user is ADMIN, CREATOR, or OWNER
        if not await is_admin_or_creator(chat_id, user_id) and not is_owner(user_id):
            await message.reply_text(USER_ERROR_MSG, reply_markup=get_owner_button())
            return
        
        if not message.reply_to_message:
            await message.reply_text(f"❌{LINE}❌\n   **__Reply to a user!__**\n❌{LINE}❌")
            return
        
        target = message.reply_to_message.from_user
        
        if target is None:
            await message.reply_text(f"❌{LINE}❌\n   **__User not found or deleted!__**\n❌{LINE}❌")
            return
        
        target_id = target.id
        
        # Check if target is OWNER
        if target_id == OWNER_ID:
            await message.reply_text(OWNER_ERROR_MSG, reply_markup=get_owner_button())
            return
        
        # Check if target is ADMIN or CREATOR
        if await is_admin_or_creator(chat_id, target_id):
            await message.reply_text(ADMIN_ERROR_MSG, reply_markup=get_owner_button())
            return
        
        if not await is_user_in_group(chat_id, target_id):
            await message.reply_text(f"❌{LINE}❌\n   **__User is not in this group!__**\n❌{LINE}❌")
            return
        
        parts = message.text.split()
        if len(parts) < 2:
            await message.reply_text(f"❌{LINE}❌\n   **__/tmkc 30s-60s/1m-60m/1w-3w/1d-30d__**\n❌{LINE}❌")
            return
        
        time_str = parts[1]
        value, unit = parse_time(time_str)
        
        if value is None:
            await message.reply_text(f"❌{LINE}❌\n   **__Invalid time!__**\n   Use: 30s-60s / 1m-60m / 1w-3w / 1d-30d\n❌{LINE}❌")
            return
        
        delta = timedelta(**{f"{unit}s": value})
        until_time = datetime.now() + delta
        until_str = until_time.isoformat()
        
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
            remove_mute(chat_id, target_id)
            await message.reply_text(f"❌{LINE}❌\n   **__Group Admin Not Mute!__**\n❌{LINE}❌")
            return
        
        admin_mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        user_mention = f"[{target.first_name}](tg://user?id={target_id})"
        duration = format_duration(value, unit)
        unmute_time = get_unmute_time(until_str)
        
        time = get_current_time()
        date = get_current_date()
        
        msg_text = MUTE_MSGS[0].format(
            user=user_mention,
            duration=duration,
            unmute_time=unmute_time,
            admin=admin_mention,
            time=time,
            date=date
        )
        
        msg_text += f"\n\n🔇 ᴍᴜᴛᴇ 🤐 ᴀᴄᴛɪᴏɴ ⛔️"
        
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

# ========== 🔴 UNMUTE COMMAND (ADMIN + CREATOR + OWNER) ==========
@app.on_message(filters.group & filters.command("tbur"))
async def unmute_user(client, message: Message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        # Check if user is revoked - delete command silently
        if is_revoked(chat_id, user_id):
            try:
                await message.delete()
            except:
                pass
            return
        
        # 🔴 FIX: Check if user is ADMIN, CREATOR, or OWNER
        if not await is_admin_or_creator(chat_id, user_id) and not is_owner(user_id):
            await message.reply_text(USER_ERROR_MSG, reply_markup=get_owner_button())
            return
        
        if not message.reply_to_message:
            await message.reply_text(f"❌{LINE}❌\n   **__Reply to a user!__**\n❌{LINE}❌")
            return
        
        target = message.reply_to_message.from_user
        
        if target is None:
            await message.reply_text(f"❌{LINE}❌\n   **__User not found or deleted!__**\n❌{LINE}❌")
            return
        
        target_id = target.id
        
        if not is_muted(chat_id, target_id):
            await message.reply_text(f"❌{LINE}❌\n   **__User is not muted!__**\n❌{LINE}❌")
            return
        
        remove_mute(chat_id, target_id)
        
        if not is_revoked(chat_id, target_id):
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
        admin_mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        
        time = get_current_time()
        date = get_current_date()
        
        msg_text = MUTE_MSGS[1].format(
            user=user_mention,
            admin=admin_mention,
            time=time,
            date=date
        )
        
        msg_text += f"\n\n🔊 ᴜɴᴍᴜᴛᴇ 🎉 ᴀᴄᴛɪᴏɴ ✅"
        
        video = get_random_video()
        if video and os.path.exists(video["path"]):
            await app.send_video(chat_id, video["path"], caption=msg_text, supports_streaming=True)
        else:
            await app.send_message(chat_id, msg_text)
        
        logger.info(f"🔊 UNMUTED: {target.first_name} by {message.from_user.first_name}")
        
    except Exception as e:
        logger.error(f"❌ Unmute error: {e}")
        await message.reply_text(f"❌ **__Error:__** {str(e)}")

# ========== REVOKE MUTE (OWNER ONLY) ==========
@app.on_message(filters.group & filters.command("revokemute"))
async def revoke_user(client, message: Message):
    try:
        if not is_owner(message.from_user.id):
            await message.reply_text(OWNER_ERROR_MSG, reply_markup=get_owner_button())
            return
        
        chat_id = message.chat.id
        
        try:
            await message.delete()
        except:
            pass
        
        if not message.reply_to_message:
            await message.reply_text(f"❌{LINE}❌\n   **__Reply to a user!__**\n❌{LINE}❌")
            return
        
        target = message.reply_to_message.from_user
        
        if target is None:
            await message.reply_text(f"❌{LINE}❌\n   **__User not found or deleted!__**\n❌{LINE}❌")
            return
        
        target_id = target.id
        
        remove_mute(chat_id, target_id)
        save_revoke(chat_id, target_id)
        
        user_mention = f"[{target.first_name}](tg://user?id={target_id})"
        admin_mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        
        time = get_current_time()
        date = get_current_date()
        
        msg_text = REVOKE_MSGS[0].format(
            user=user_mention,
            admin=admin_mention,
            time=time,
            date=date
        )
        
        msg_text += f"\n\n🔇 ʀᴇᴠᴏᴋᴇ 🚫 ᴅᴇʟᴇᴛᴇ 🗑️"
        
        video = get_random_video()
        if video and os.path.exists(video["path"]):
            await app.send_video(chat_id, video["path"], caption=msg_text, supports_streaming=True)
        else:
            await app.send_message(chat_id, msg_text)
        
        logger.info(f"🔇 REVOKED: {target.first_name}")
        
    except Exception as e:
        logger.error(f"❌ Revoke error: {e}")

# ========== UNREVOKE MUTE (OWNER ONLY) ==========
@app.on_message(filters.group & filters.command("unrevokemute"))
async def unrevoke_user(client, message: Message):
    try:
        if not is_owner(message.from_user.id):
            await message.reply_text(OWNER_ERROR_MSG, reply_markup=get_owner_button())
            return
        
        chat_id = message.chat.id
        
        try:
            await message.delete()
        except:
            pass
        
        target = None
        target_id = None
        
        if message.reply_to_message:
            target = message.reply_to_message.from_user
            if target:
                target_id = target.id
        
        if target is None:
            parts = message.text.split()
            if len(parts) >= 2:
                input_str = parts[1]
                target = await get_user_from_input(app, input_str, chat_id)
                if target:
                    target_id = target.id
        
        if target is None or target_id is None:
            await message.reply_text(f"❌{LINE}❌\n   **__Reply to a user or provide ID/Username!__**\n   **__Usage: /unrevokemute 123456789__**\n❌{LINE}❌")
            return
        
        if not remove_revoke(chat_id, target_id):
            await message.reply_text(f"❌{LINE}❌\n   **__User is not revoked!__**\n❌{LINE}❌")
            return
        
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
        admin_mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
        
        time = get_current_time()
        date = get_current_date()
        
        msg_text = REVOKE_MSGS[1].format(
            user=user_mention,
            admin=admin_mention,
            time=time,
            date=date
        )
        
        msg_text += f"\n\n🔊 ᴜɴʀᴇᴠᴏᴋᴇ ✅ ʀᴇsᴛᴏʀᴇ 🎉"
        
        video = get_random_video()
        if video and os.path.exists(video["path"]):
            await app.send_video(chat_id, video["path"], caption=msg_text, supports_streaming=True)
        else:
            await app.send_message(chat_id, msg_text)
        
        logger.info(f"🔊 UNREVOKED: {target.first_name} (ID: {target_id})")
        
    except Exception as e:
        logger.error(f"❌ Unrevoke error: {e}")
        await message.reply_text(f"❌ **__Error:__** {str(e)}")

# ========== REVOKED USER LIST ==========
@app.on_message(filters.group & filters.command("revokemutelist") & filters.user(OWNER_ID))
async def revoke_list(client, message: Message):
    try:
        chat_id = message.chat.id
        
        try:
            await message.delete()
        except:
            pass
        
        revoked_users = get_revoked_users(chat_id)
        
        if not revoked_users:
            await message.reply_text(f"📭{LINE}📭\n   **__No revoked users!__**\n📭{LINE}📭")
            return
        
        text = f"🔇 **__Revoked Users__**\n\n{LINE}\n"
        for user_id in revoked_users:
            try:
                user = await app.get_users(user_id)
                text += f"• {user.first_name} (`{user_id}`)\n"
            except:
                text += f"• Unknown User (`{user_id}`)\n"
        text += f"\n{LINE}"
        
        await message.reply_text(text)
        
    except Exception as e:
        logger.error(f"❌ Revoke list error: {e}")
        await message.reply_text(f"❌ **__Error:__** {str(e)}")

# ========== AUTO UNMUTE ==========
async def auto_unmute(chat_id, user_id, user_name, until_time):
    try:
        now = datetime.now()
        wait_seconds = (until_time - now).total_seconds()
        
        if wait_seconds < 0:
            wait_seconds = 0
        
        logger.info(f"⏳ Auto-unmute: {user_name} will unmute in {wait_seconds} seconds")
        
        if wait_seconds > 0:
            await asyncio.sleep(wait_seconds)
        
        if is_revoked(chat_id, user_id):
            logger.info(f"🔇 User {user_name} is revoked, skipping auto-unmute")
            return
        
        is_restricted = False
        try:
            member = await app.get_chat_member(chat_id, user_id)
            if member.status == "restricted" and not member.can_send_messages:
                is_restricted = True
                logger.info(f"🔊 User {user_name} is still restricted")
        except Exception as e:
            logger.info(f"ℹ️ Could not check user status: {e}")
        
        remove_mute(chat_id, user_id)
        
        if is_restricted:
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
                logger.info(f"🔊 Auto-unmuted: {user_name}")
            except Exception as e:
                logger.error(f"❌ Auto-unmute restrict error: {e}")
        else:
            logger.info(f"ℹ️ User {user_name} is already unmuted, but sending notification anyway")
        
        user_mention = f"[{user_name}](tg://user?id={user_id})"
        time = get_current_time()
        date = get_current_date()
        
        msg_text = MUTE_MSGS[2].format(
            user=user_mention,
            time=time,
            date=date
        )
        
        msg_text += f"\n\n🔊 ᴀᴜᴛᴏ 🤖 ᴜɴᴍᴜᴛᴇ ✅"
        
        video = get_random_video()
        if video and os.path.exists(video["path"]):
            try:
                await app.send_video(chat_id, video["path"], caption=msg_text, supports_streaming=True)
                logger.info(f"📹 Auto-unmute video sent for {user_name}")
            except Exception as e:
                logger.error(f"❌ Auto-unmute video error: {e}")
                await app.send_message(chat_id, msg_text)
        else:
            await app.send_message(chat_id, msg_text)
        
        logger.info(f"🔊 AUTO UNMUTED: {user_name}")
            
    except asyncio.CancelledError:
        logger.info(f"⏹️ Auto-unmute cancelled for {user_name}")
    except Exception as e:
        logger.error(f"❌ Auto unmute error: {e}")
        try:
            user_mention = f"[{user_name}](tg://user?id={user_id})"
            time = get_current_time()
            date = get_current_date()
            msg_text = MUTE_MSGS[2].format(user=user_mention, time=time, date=date)
            msg_text += f"\n\n🔊 ᴀᴜᴛᴏ 🤖 ᴜɴᴍᴜᴛᴇ ✅"
            await app.send_message(chat_id, msg_text)
        except:
            pass

# ========== DELETE REVOKED USER MESSAGES ==========
@app.on_message(filters.group & (filters.text | filters.photo | filters.video | filters.document | filters.sticker | filters.voice | filters.video_note | filters.audio | filters.animation))
async def delete_revoked_messages(client, message: Message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        if is_revoked(chat_id, user_id):
            await message.delete()
            logger.info(f"🗑️ Deleted message from revoked user: {message.from_user.first_name}")
            return
        
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
            UNAUTHORIZED_MSG.format(
                user=message.from_user.first_name,
                time=get_current_time(),
                date=get_current_date()
            ),
            reply_markup=get_owner_button()
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
• `/tmkc` - **__ᴛᴇᴍᴘ__**
• `/tbur` - **__ᴜɴᴍᴜᴛᴇ__**
• `/revokemute` - **__ʀᴇᴠᴏᴋᴇ__**
• `/unrevokemute` - **__ᴜɴʀᴇᴠᴏᴋᴇ__**
• `/revokemutelist` - **__ʀᴇᴠᴏᴋᴇᴅ ʟɪsᴛ__**

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
