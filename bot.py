from pyrogram import Client, filters

# 🔴 YAHAN APNA DATA DAALO
API_ID = 35140329  # my.telegram.org se
API_HASH = "011f638e4acadee178c59afffc80193d"  # my.telegram.org se
BOT_TOKEN = "8988202401:AAFagkU0KwAPiEesXrE9ND3rVRdlJmf4guo"  # @BotFather se

app = Client("test_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("✅ **Bot is working!** 🎉")

@app.on_message(filters.text)
async def echo(client, message):
    await message.reply_text(f"📝 You said: {message.text}")

print("🚀 Testing bot...")
print("Send /start to your bot")

app.run()
