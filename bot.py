import logging
import json
import random
import os
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated

# ========== LOGGING ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== 🔴 YAHAN APNA DATA DAALO ==========
API_ID = 35140329  # 🔴 my.telegram.org se
API_HASH = "011f638e4acadee178c59afffc80193d"  # 🔴 my.telegram.org se
BOT_TOKEN = "8603632286:AAE8Hw5xWzKjrpr4r7PrrMifZxu7-v93TaM"  # 🔴 @BotFather se (SIRF EK BOT - MAIN BOT)

# ========== DATABASE ==========
VIDEO_DB = "videos.json"

# ========== VIDEO FUNCTIONS ==========
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
    videos.append({
        "path": video_path,
        "timestamp": datetime.now().isoformat(),
        "used": False
    })
    with open(VIDEO_DB, "w") as f:
        json.dump(videos, f, indent=2)
    logger.info(f"✅ Video saved: {video_path}")

def get_unused_video():
    videos = load_videos()
    if not videos:
        return None
    
    unused = [v for v in videos if not v.get("used", False)]
    if unused:
        video = random.choice(unused)
        for v in videos:
            if v["path"] == video["path"]:
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

# ========== PREMIUM MESSAGES ==========
JOIN_MESSAGES = [
    """🌟━━━━━━━━━━━━━━━━━🌟
┏━━━━━━━━━━━━━━━━━┓
┃ ✨ **{user}** ✨
┃ 🎯 **JOINED** the group!
┗━━━━━━━━━━━━━━━━━┛
🌟━━━━━━━━━━━━━━━━━🌟

🎉 **ᴡᴇʟᴄᴏᴍᴇ** ᴛᴏ ᴛʜᴇ **ᴘʀᴇᴍɪᴜᴍ** ғᴀᴍɪʟʏ! 🏆
💎 **ʏᴏᴜ'ʀᴇ** ᴛʜᴇ **ʙᴇsᴛ** ᴀᴅᴅɪᴛɪᴏɴ ᴛᴏᴅᴀʏ! 🔥""",

    """💫━━━━━━━━━━━━━━━━━💫
╔━━━━━━━━━━━━━━━━━╗
║ 🚀 **{user}** 🚀
║ 👑 **ENTERED** the arena!
╚━━━━━━━━━━━━━━━━━╝
💫━━━━━━━━━━━━━━━━━💫

🌟 **ɴᴇᴡ ᴘʟᴀʏᴇʀ** ɪɴ ᴛʜᴇ ʜᴏᴜsᴇ! 🎮
⚡️ **ᴡᴇ'ʀᴇ** sᴏ **ᴇxᴄɪᴛᴇᴅ** ᴛᴏ ʜᴀᴠᴇ ʏᴏᴜ! 💫"""
]

LEFT_MESSAGES = [
    """😔━━━━━━━━━━━━━━━━━😔
┏━━━━━━━━━━━━━━━━━┓
┃ 💔 **{user}** 💔
┃ 🚶 **LEFT** the group!
┗━━━━━━━━━━━━━━━━━┛
😔━━━━━━━━━━━━━━━━━😔

🕊️ **ᴡᴇ'ʟʟ** ᴍɪss ʏᴏᴜ **ᴅᴇᴀʀ** ғʀɪᴇɴᴅ! 💫
🌈 **ɢᴏᴏᴅʙʏᴇ** ᴀɴᴅ **ᴛᴀᴋᴇ** ᴄᴀʀᴇ! 🌟"""
]

BAN_MESSAGES = [
    """🚫━━━━━━━━━━━━━━━━━🚫
┏━━━━━━━━━━━━━━━━━┓
┃ ⛔️ **{user}** ⛔️
┃ 🔨 **BANNED** from group!
┗━━━━━━━━━━━━━━━━━┛
🚫━━━━━━━━━━━━━━━━━🚫

⚖️ **ʀᴜʟᴇs** ᴡᴇʀᴇ **ʙʀᴏᴋᴇɴ**! 🚨
❌ **ᴀᴄᴛɪᴏɴ** ʜᴀs ʙᴇᴇɴ **ᴛᴀᴋᴇɴ**! 💥"""
]

# ========== BOT CREATE ==========
print("🔧 Creating bot...")

app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("✅ Bot created!")

# ========== COMMAND HANDLERS ==========

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    logger.info(f"📩 /start from {message.from_user.first_name}")
    await message.reply_text(
        f"""🌟 **ᴘʀᴇᴍɪᴜᴍ ɢʀᴏᴜᴘ ʙᴏᴛ** 🌟

**ʜᴇʏ** {message.from_user.first_name}! 👋

✅ Bot is **working** properly!

📹 **ᴛᴏᴛᴀʟ ᴠɪᴅᴇᴏs:** {get_video_count()}

**ғᴇᴀᴛᴜʀᴇs:**
• 🎯 Auto welcome for new members
• 💔 Auto goodbye for left members
• 🚫 Auto ban notifications
• 📹 Video with every notification

**ᴄᴏᴍᴍᴀɴᴅs:**
• `/save` - Save video (reply to video)
• `/videos` - View all videos
• `/delete` - Delete video
• `/clear` - Clear all videos
• `/stats` - View statistics

💎 **ᴘʀᴇᴍɪᴜᴍ** ʙᴏᴛ 💎"""
    )

@app.on_message(filters.command("ping") & filters.private)
async def ping_command(client, message):
    logger.info(f"📩 /ping from {message.from_user.first_name}")
    await message.reply_text("🏓 **Pong!** Bot is alive!")

@app.on_message(filters.command("save") & filters.private)
async def save_video_command(client, message):
    status = await message.reply_text("⏳ **sᴀᴠɪɴɢ ᴠɪᴅᴇᴏ...**")
    
    try:
        if message.reply_to_message and message.reply_to_message.video:
            video_path = await message.reply_to_message.download()
            save_video(video_path)
            await status.edit_text(
                f"✅ **ᴠɪᴅᴇᴏ sᴀᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!** 🎉\n\n"
                f"📹 **ᴛᴏᴛᴀʟ ᴠɪᴅᴇᴏs:** {get_video_count()}"
            )
        else:
            await status.edit_text("❌ **ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ!**\n\nSend video and reply with `/save`")
    except Exception as e:
        await status.edit_text(f"❌ **ᴇʀʀᴏʀ:** {str(e)}")

@app.on_message(filters.command("videos") & filters.private)
async def list_videos(client, message):
    videos = load_videos()
    if not videos:
        await message.reply_text("❌ **ɴᴏ ᴠɪᴅᴇᴏs ғᴏᴜɴᴅ!**\n\nSend video and reply with `/save`")
        return
    
    text = f"🎬 **ᴛᴏᴛᴀʟ ᴠɪᴅᴇᴏs:** {len(videos)}\n\n"
    text += "━━━━━━━━━━━━━━━━━\n"
    for i, video in enumerate(videos[:20], 1):
        used = "✅" if video.get("used", False) else "🔄"
        text += f"{used} **{i}.** `{os.path.basename(video['path'])}`\n"
        text += f"   🕐 `{video['timestamp'][:16]}`\n"
        text += "━━━━━━━━━━━━━━━━━\n"
    
    if len(videos) > 20:
        text += f"\n... ᴀɴᴅ {len(videos) - 20} ᴍᴏʀᴇ\n"
    
    text += f"\n💡 **ᴜsᴀɢᴇ:** `/delete 1` ᴛᴏ ᴅᴇʟᴇᴛᴇ"
    await message.reply_text(text)

@app.on_message(filters.command("delete") & filters.private)
async def delete_video(client, message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            await message.reply_text("❌ **ᴜsᴀɢᴇ:** `/delete 1`")
            return
        
        index = int(parts[1]) - 1
        videos = load_videos()
        
        if 0 <= index < len(videos):
            deleted = videos.pop(index)
            with open(VIDEO_DB, "w") as f:
                json.dump(videos, f, indent=2)
            
            if os.path.exists(deleted["path"]):
                os.remove(deleted["path"])
            
            await message.reply_text(
                f"✅ **ᴠɪᴅᴇᴏ ᴅᴇʟᴇᴛᴇᴅ!** 🗑️\n\n"
                f"📹 **ʀᴇᴍᴀɪɴɪɴɢ:** {len(videos)}"
            )
        else:
            await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ!**")
    except:
        await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ғᴏʀᴍᴀᴛ!**")

@app.on_message(filters.command("clear") & filters.private)
async def clear_videos(client, message):
    videos = load_videos()
    if not videos:
        await message.reply_text("❌ **ɴᴏ ᴠɪᴅᴇᴏs ᴛᴏ ᴄʟᴇᴀʀ!**")
        return
    
    for video in videos:
        if os.path.exists(video["path"]):
            os.remove(video["path"])
    
    with open(VIDEO_DB, "w") as f:
        json.dump([], f)
    
    await message.reply_text(
        f"🗑️ **ᴀʟʟ ᴠɪᴅᴇᴏs ᴄʟᴇᴀʀᴇᴅ!**\n\n"
        f"📹 **ʀᴇᴍᴏᴠᴇᴅ:** {len(videos)} ᴠɪᴅᴇᴏs"
    )

@app.on_message(filters.command("stats") & filters.private)
async def stats_command(client, message):
    videos = load_videos()
    total_size = 0
    used = 0
    
    for video in videos:
        if os.path.exists(video["path"]):
            total_size += os.path.getsize(video["path"])
        if video.get("used", False):
            used += 1
    
    text = f"""📊 **ᴠɪᴅᴇᴏ sᴛᴀᴛɪsᴛɪᴄs**

━━━━━━━━━━━━━━━━━
📹 **ᴛᴏᴛᴀʟ ᴠɪᴅᴇᴏs:** `{len(videos)}`
🔄 **ᴜɴᴜsᴇᴅ:** `{len(videos) - used}`
✅ **ᴜsᴇᴅ:** `{used}`
💾 **ᴛᴏᴛᴀʟ sɪᴢᴇ:** `{total_size / (1024*1024):.2f} MB`
━━━━━━━━━━━━━━━━━
💎 **ᴘʀᴇᴍɪᴜᴍ** sᴛᴏʀᴀɢᴇ 💎"""
    
    await message.reply_text(text)

# ========== JOIN/LEFT/BAN HANDLER ==========
async def send_premium_notification(chat_id, user_mention, message_template):
    try:
        msg_text = message_template.format(user=user_mention)
        emojis = ["🔥", "✨", "💎", "🌟", "🎉", "🚀"]
        footer = random.sample(emojis, 3)
        msg_text += f"\n\n{footer[0]} **ᴘʀᴇᴍɪᴜᴍ** {footer[1]} **ᴜᴘᴅᴀᴛᴇ** {footer[2]}"
        msg_text += f"\n🕐 `{datetime.now().strftime('%H:%M:%S')}`"
        
        video_data = get_unused_video()
        
        if video_data and os.path.exists(video_data["path"]):
            await app.send_video(
                chat_id=chat_id,
                video=video_data["path"],
                caption=msg_text,
                supports_streaming=True
            )
            logger.info(f"📹 Video sent: {video_data['path']}")
        else:
            await app.send_message(chat_id=chat_id, text=msg_text)
            logger.info("📝 Message sent (no video)")
    except Exception as e:
        logger.error(f"❌ Error: {e}")

@app.on_chat_member_updated()
async def member_update_handler(client, update: ChatMemberUpdated):
    try:
        chat_id = update.chat.id
        
        if update.new_chat_member and not update.old_chat_member:
            user = update.new_chat_member.user
            mention = f"[{user.first_name}](tg://user?id={user.id})"
            await send_premium_notification(chat_id, mention, random.choice(JOIN_MESSAGES))
            logger.info(f"👤 JOIN: {user.first_name}")
        
        elif update.old_chat_member and not update.new_chat_member:
            user = update.old_chat_member.user
            mention = f"[{user.first_name}](tg://user?id={user.id})"
            await send_premium_notification(chat_id, mention, random.choice(LEFT_MESSAGES))
            logger.info(f"🚶 LEFT: {user.first_name}")
        
        elif update.new_chat_member and update.new_chat_member.status in ["kicked", "restricted"]:
            user = update.new_chat_member.user
            mention = f"[{user.first_name}](tg://user?id={user.id})"
            await send_premium_notification(chat_id, mention, random.choice(BAN_MESSAGES))
            logger.info(f"🚫 BANNED: {user.first_name}")
    except Exception as e:
        logger.error(f"❌ Error in member update: {e}")

# ========== ON STARTUP ==========
@app.on_message(filters.command("start") & filters.group)
async def group_start(client, message):
    await message.reply_text("✅ **Bot is active in this group!**")

# ========== RUN BOT ==========
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 STARTING BOT...")
    print("="*50 + "\n")
    
    # Create database
    if not os.path.exists(VIDEO_DB):
        with open(VIDEO_DB, "w") as f:
            json.dump([], f)
    
    # Create downloads folder
    os.makedirs("downloads", exist_ok=True)
    
    try:
        # 🔴 YEH SABSE IMPORTANT HAI - app.run() USE KARO
        app.run()
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
