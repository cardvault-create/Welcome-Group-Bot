import asyncio
import json
import random
import os
import logging
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import ChatMemberUpdated
from pyrogram.errors import FloodWait

# ========== LOGGING ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== CONFIGURATION ==========
# 🔴 APNA DATA DAALO
API_ID = 12345
API_HASH = "your_api_hash"

# 🔴 DO ALAG BOT TOKENS
MAIN_BOT_TOKEN = "8603632286:AAHD-EKEJKpWXoOYZTbJOsQd9dCTVLxPEnI"  # Group notification bot
VIDEO_BOT_TOKEN = "8669835210:AAGzM4EZz3FNuIN4ce4IUZzY8-5L5B-C-VE"  # Video storage bot

# Database file
VIDEO_DB = "videos.json"

# ========== VIDEO DATABASE FUNCTIONS ==========
def load_videos():
    """Load all videos from database"""
    try:
        if os.path.exists(VIDEO_DB):
            with open(VIDEO_DB, "r") as f:
                return json.load(f)
    except:
        pass
    return []

def save_video(video_path, video_id=None):
    """Save video to database"""
    videos = load_videos()
    videos.append({
        "path": video_path,
        "id": video_id or len(videos) + 1,
        "timestamp": datetime.now().isoformat(),
        "used": False
    })
    with open(VIDEO_DB, "w") as f:
        json.dump(videos, f, indent=2)
    logger.info(f"✅ Video saved: {video_path}")
    return len(videos) - 1

def get_unused_video():
    """Get a video that hasn't been used recently"""
    videos = load_videos()
    if not videos:
        return None
    
    # Try to get unused video first
    unused = [v for v in videos if not v.get("used", False)]
    if unused:
        video = random.choice(unused)
        # Mark as used
        for v in videos:
            if v["path"] == video["path"]:
                v["used"] = True
        with open(VIDEO_DB, "w") as f:
            json.dump(videos, f, indent=2)
        return video
    
    # If all used, reset and return random
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
⚡️ **ᴡᴇ'ʀᴇ** sᴏ **ᴇxᴄɪᴛᴇᴅ** ᴛᴏ ʜᴀᴠᴇ ʏᴏᴜ! 💫""",

    """🔥━━━━━━━━━━━━━━━━━🔥
╔━━━━━━━━━━━━━━━━━╗
║ ⭐️ **{user}** ⭐️
║ 🎊 **WELCOME** aboard!
╚━━━━━━━━━━━━━━━━━╝
🔥━━━━━━━━━━━━━━━━━🔥

🌈 **ɴᴇᴡ** ᴍᴇᴍʙᴇʀ **ᴜɴʟᴏᴄᴋᴇᴅ**! 🗝️
💫 **ᴛʜᴇ** ғᴀᴍɪʟʏ **ɢʀᴏᴡs** ʙʏ ᴏɴᴇ! 🎉"""
]

LEFT_MESSAGES = [
    """😔━━━━━━━━━━━━━━━━━😔
┏━━━━━━━━━━━━━━━━━┓
┃ 💔 **{user}** 💔
┃ 🚶 **LEFT** the group!
┗━━━━━━━━━━━━━━━━━┛
😔━━━━━━━━━━━━━━━━━😔

🕊️ **ᴡᴇ'ʟʟ** ᴍɪss ʏᴏᴜ **ᴅᴇᴀʀ** ғʀɪᴇɴᴅ! 💫
🌈 **ɢᴏᴏᴅʙʏᴇ** ᴀɴᴅ **ᴛᴀᴋᴇ** ᴄᴀʀᴇ! 🌟""",

    """🌧️━━━━━━━━━━━━━━━━━🌧️
╔━━━━━━━━━━━━━━━━━╗
║ 👋 **{user}** 👋
║ 🚪 **EXITED** the group!
╚━━━━━━━━━━━━━━━━━╝
🌧️━━━━━━━━━━━━━━━━━🌧️

😢 **sᴀᴅ** ᴛᴏ sᴇᴇ ʏᴏᴜ **ʟᴇᴀᴠᴇ**! 💔
🌟 **ʏᴏᴜ'ʟʟ** ʙᴇ **ᴍɪssᴇᴅ** ʜᴇʀᴇ! 🥺"""
]

BAN_MESSAGES = [
    """🚫━━━━━━━━━━━━━━━━━🚫
┏━━━━━━━━━━━━━━━━━┓
┃ ⛔️ **{user}** ⛔️
┃ 🔨 **BANNED** from group!
┗━━━━━━━━━━━━━━━━━┛
🚫━━━━━━━━━━━━━━━━━🚫

⚖️ **ʀᴜʟᴇs** ᴡᴇʀᴇ **ʙʀᴏᴋᴇɴ**! 🚨
❌ **ᴀᴄᴛɪᴏɴ** ʜᴀs ʙᴇᴇɴ **ᴛᴀᴋᴇɴ**! 💥""",

    """🔒━━━━━━━━━━━━━━━━━🔒
╔━━━━━━━━━━━━━━━━━╗
║ 🚷 **{user}** 🚷
║ 🔐 **PERMANENTLY** banned!
╚━━━━━━━━━━━━━━━━━╝
🔒━━━━━━━━━━━━━━━━━🔒

⛓️ **sᴇᴄᴜʀɪᴛʏ** ᴍᴇᴀsᴜʀᴇs **ᴀᴄᴛɪᴠᴀᴛᴇᴅ**! 🛡️
🗑️ **ʀᴇᴍᴏᴠᴇᴅ** ғʀᴏᴍ ᴛʜᴇ **ᴄᴏᴍᴍᴜɴɪᴛʏ**! ❌"""
]

# ========== MAIN BOT (GROUP NOTIFICATION) ==========
main_app = Client(
    "main_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=MAIN_BOT_TOKEN
)

# ========== VIDEO BOT (STORAGE) ==========
video_app = Client(
    "video_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=VIDEO_BOT_TOKEN
)

# ========== MAIN BOT HANDLERS ==========

async def send_premium_notification(chat_id, user_mention, message_template):
    """Send premium notification with video"""
    try:
        msg_text = message_template.format(user=user_mention)
        
        # Add premium footer
        emojis = ["🔥", "✨", "💎", "🌟", "🎉", "🚀", "👑", "💫"]
        footer = random.sample(emojis, 3)
        msg_text += f"\n\n{footer[0]} **ᴘʀᴇᴍɪᴜᴍ** {footer[1]} **ᴜᴘᴅᴀᴛᴇ** {footer[2]}"
        msg_text += f"\n🕐 `{datetime.now().strftime('%H:%M:%S')}`"
        
        # Get unused video
        video_data = get_unused_video()
        
        if video_data and os.path.exists(video_data["path"]):
            # Send video
            await main_app.send_video(
                chat_id=chat_id,
                video=video_data["path"],
                caption=msg_text,
                supports_streaming=True,
                width=1920,
                height=1080
            )
            logger.info(f"📹 Video sent: {video_data['path']}")
        else:
            # Send only message
            await main_app.send_message(chat_id=chat_id, text=msg_text)
            logger.info("📝 Message sent (no video)")
            
    except FloodWait as e:
        await asyncio.sleep(e.x)
    except Exception as e:
        logger.error(f"❌ Error: {e}")

@main_app.on_chat_member_updated()
async def member_update_handler(client, update: ChatMemberUpdated):
    chat_id = update.chat.id
    
    # New Member Join
    if update.new_chat_member and not update.old_chat_member:
        user = update.new_chat_member.user
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        msg = random.choice(JOIN_MESSAGES)
        await send_premium_notification(chat_id, mention, msg)
        logger.info(f"👤 JOIN: {user.first_name}")
    
    # Member Left
    elif update.old_chat_member and not update.new_chat_member:
        user = update.old_chat_member.user
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        msg = random.choice(LEFT_MESSAGES)
        await send_premium_notification(chat_id, mention, msg)
        logger.info(f"🚶 LEFT: {user.first_name}")
    
    # Member Banned
    elif update.new_chat_member and update.new_chat_member.status in ["kicked", "restricted"]:
        user = update.new_chat_member.user
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        msg = random.choice(BAN_MESSAGES)
        await send_premium_notification(chat_id, mention, msg)
        logger.info(f"🚫 BANNED: {user.first_name}")

# ========== VIDEO BOT COMMANDS ==========

@video_app.on_message(filters.command("start") & filters.private)
async def video_start(client, message):
    await message.reply_text(
        f"""📹 **ᴠɪᴅᴇᴏ sᴛᴏʀᴀɢᴇ ʙᴏᴛ** 🎬

**ʜᴇʏ** {message.from_user.first_name}! 👋

**ʜᴏᴡ ᴛᴏ ᴜsᴇ:**
1. 📤 Send me a **video**
2. 📝 Reply with `/save`
3. ✅ Video will be saved

**ᴄᴜʀʀᴇɴᴛ ᴠɪᴅᴇᴏs:** {get_video_count()}

**ᴄᴏᴍᴍᴀɴᴅs:**
• `/save` - Save video
• `/videos` - View all videos
• `/delete` - Delete video
• `/clear` - Clear all videos
• `/stats` - View statistics

💎 **ᴘʀᴇᴍɪᴜᴍ** sᴛᴏʀᴀɢᴇ 💎"""
    )

@video_app.on_message(filters.command("save") & filters.private)
async def save_video_command(client, message):
    """Save video to database"""
    status = await message.reply_text("⏳ **sᴀᴠɪɴɢ ᴠɪᴅᴇᴏ...**")
    
    try:
        if message.reply_to_message and message.reply_to_message.video:
            # Download video
            video_path = await message.reply_to_message.download()
            
            # Save to database
            save_video(video_path)
            
            await status.edit_text(
                f"✅ **ᴠɪᴅᴇᴏ sᴀᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!** 🎉\n\n"
                f"📹 **ᴛᴏᴛᴀʟ ᴠɪᴅᴇᴏs:** {get_video_count()}\n"
                f"🔄 **ɴᴇxᴛ ᴊᴏɪɴ/ʟᴇғᴛ/ʙᴀɴ** ᴡɪʟʟ ᴜsᴇ ᴛʜɪs ᴠɪᴅᴇᴏ!"
            )
        else:
            await status.edit_text(
                "❌ **ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ!**\n\n"
                "**ᴜsᴀɢᴇ:** Send video → Reply with `/save`"
            )
    except Exception as e:
        await status.edit_text(f"❌ **ᴇʀʀᴏʀ:** {str(e)}")

@video_app.on_message(filters.command("videos") & filters.private)
async def list_videos(client, message):
    """List all saved videos"""
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

@video_app.on_message(filters.command("delete") & filters.private)
async def delete_video(client, message):
    """Delete specific video"""
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

@video_app.on_message(filters.command("clear") & filters.private)
async def clear_videos(client, message):
    """Clear all videos"""
    videos = load_videos()
    if not videos:
        await message.reply_text("❌ **ɴᴏ ᴠɪᴅᴇᴏs ᴛᴏ ᴄʟᴇᴀʀ!**")
        return
    
    # Delete files
    for video in videos:
        if os.path.exists(video["path"]):
            os.remove(video["path"])
    
    # Clear database
    with open(VIDEO_DB, "w") as f:
        json.dump([], f)
    
    await message.reply_text(
        f"🗑️ **ᴀʟʟ ᴠɪᴅᴇᴏs ᴄʟᴇᴀʀᴇᴅ!**\n\n"
        f"📹 **ʀᴇᴍᴏᴠᴇᴅ:** {len(videos)} ᴠɪᴅᴇᴏs"
    )

@video_app.on_message(filters.command("stats") & filters.private)
async def stats_command(client, message):
    """Show statistics"""
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

# ========== KEEP ALIVE ==========
async def keep_alive():
    """Keep bots alive"""
    while True:
        await asyncio.sleep(300)
        logger.info("💓 Keep-alive ping")
        try:
            await main_app.get_me()
            await video_app.get_me()
        except:
            pass

# ========== MAIN FUNCTION ==========
async def main():
    logger.info("🚀 Starting Premium Bots...")
    
    # Create database
    if not os.path.exists(VIDEO_DB):
        with open(VIDEO_DB, "w") as f:
            json.dump([], f)
    
    # Create downloads folder
    os.makedirs("downloads", exist_ok=True)
    
    # Start both bots
    await main_app.start()
    await video_app.start()
    
    # Start keep alive
    asyncio.create_task(keep_alive())
    
    logger.info("✅ Both bots started successfully!")
    logger.info(f"📹 Total videos: {get_video_count()}")
    logger.info("💎 Premium Bot is ready!")
    
    # Keep running
    await asyncio.Event().wait()

# ========== RUN ==========
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bots stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
