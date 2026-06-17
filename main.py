import os
import logging
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

# ফ্ল্যাস্ক সার্ভার সেটআপ (রেন্ডারের জন্য)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running perfectly!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# বটের কমান্ড
async def start(update, context):
    await update.message.reply_text("হ্যালো! আমি আপনার ট্রেডিং অ্যাসিস্ট্যান্ট। আমি প্রস্তুত।")

if __name__ == '__main__':
    # ওয়েব সার্ভার আলাদা থ্রেডে চালু
    Thread(target=run_web).start()
    
    # আপনার টোকেনটি রেন্ডারের এনভায়রনমেন্ট থেকে নেবে
    TOKEN = os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        print("Error: BOT_TOKEN not found!")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        print("Bot is polling...")
        application.run_polling()
