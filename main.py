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

async def signal(update, context):
    try:
        # লাইভ ডাটা আনা
        ticker = yf.Ticker("EURUSD=X")
        data = ticker.history(period="1d", interval="15m")
        price = data['Close'].iloc[-1]
        
        # একটি সিম্পল লজিক (আপনি পরে এখানে RSI ক্যালকুলেশন যোগ করবেন)
        # আপাতত আমরা ধরে নিচ্ছি price ২ মিনিটের জন্য সিগন্যাল দিচ্ছে
        signal_msg = (f"📊 লাইভ মার্কেট সিগন্যাল (EUR/USD)\n"
                      f"💵 বর্তমান প্রাইস: {price:.5f}\n"
                      f"🚀 পরামর্শ: মার্কেট অস্থির, এন্ট্রি নেওয়ার আগে চার্ট দেখুন!")
        
        await update.message.reply_text(signal_msg)
    except Exception as e:
        await update.message.reply_text("ডাটা আনতে সমস্যা হচ্ছে, পরে আবার চেষ্টা করুন।")

if __name__ == '__main__':
    Thread(target=run_web).start()
    TOKEN = os.getenv("BOT_TOKEN")
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("signal", signal))
    application.run_polling()
