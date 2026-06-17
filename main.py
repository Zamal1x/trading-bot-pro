import os
import yfinance as yf
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

# সিগন্যাল ফাংশন
async def signal(update, context):
    try:
        # EUR/USD এর লাইভ ডাটা
        ticker = yf.Ticker("EURUSD=X")
        data = ticker.history(period="1d", interval="15m")
        price = data['Close'].iloc[-1]
        
        await update.message.reply_text(f"📊 লাইভ মার্কেট সিগন্যাল (EUR/USD)\n💵 বর্তমান প্রাইস: {price:.5f}\n🚀 এন্ট্রি: বর্তমান প্রাইসে দেখুন\n💡 সতর্কবার্তা: ট্রেড নেওয়ার আগে নিজে যাচাই করুন।")
    except Exception as e:
        await update.message.reply_text("দুঃখিত, ডাটা আনতে সমস্যা হচ্ছে।")

if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = os.getenv("BOT_TOKEN")
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("signal", signal))
    
    application.run_polling()
