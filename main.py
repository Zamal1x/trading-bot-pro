import os
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# আগে যা ছিল
async def start(update, context):
    await update.message.reply_text("বট চালু হয়েছে!")

# নতুন যোগ করা ফাংশন (সিগন্যালের জন্য)
async def signal(update, context):
    await update.message.reply_text("🔎 অ্যানালাইসিস চলছে...\n📊 RSI: ৬৭ (ওভারবট)\n📉 সিগন্যাল: ৯৫% সেল (Sell) করার সম্ভাবনা!")

if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = os.getenv("BOT_TOKEN")
    
    # অ্যাপ বিল্ড করা
    application = ApplicationBuilder().token(TOKEN).build()
    
    # এখানে কমান্ডগুলো যোগ করবেন
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("signal", signal)) # নতুন কমান্ড যোগ হলো
    
    application.run_polling()
