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

async def start(update, context):
    await update.message.reply_text("বট চালু হয়েছে!")

async def signal(update, context):
    await update.message.reply_text("📊 লাইভ সিগন্যাল: চেক করছি...")

if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("CRITICAL ERROR: BOT_TOKEN not found!")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("signal", signal))
        application.run_polling()
