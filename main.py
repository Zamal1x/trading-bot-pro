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

if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
