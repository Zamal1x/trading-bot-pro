import os
import logging
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler
from tradingview_ta import TA_Handler, Interval, Exchange

# লগিং সেটআপ যাতে কোনো সমস্যা হলে লগে দেখতে পারেন
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

async def signal(update, context):
    try:
        # ট্রেডিং ভিউ সিগন্যাল লজিক
        handler = TA_Handler(
            symbol="EURUSD",
            screener="forex",
            exchange="FX_IDC",
            interval=Interval.INTERVAL_1_MINUTE
        )
        analysis = handler.get_analysis()
        summary = analysis.summary
        
        signal_msg = (f"📊 ট্রেডিং ভিউ সিগন্যাল (EUR/USD)\n"
                      f"📈 সুপারিশ: {summary['RECOMMENDATION']}\n"
                      f"✅ বাই: {summary['BUY']} | ❌ সেল: {summary['SELL']} | ⚪ নিউট্রাল: {summary['NEUTRAL']}\n"
                      f"⚠️ সিদ্ধান্ত নেওয়ার আগে নিজে যাচাই করুন।")
        
        await update.message.reply_text(signal_msg)
    except Exception as e:
        await update.message.reply_text(f"এরর হয়েছে: {str(e)}")

if __name__ == '__main__':
    # ওয়েব সার্ভার চালু করা
    Thread(target=run_web).start()
    
    # বট টোকেন চেক করা
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("CRITICAL ERROR: BOT_TOKEN not found!")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler("signal", signal))
        application.run_polling()
