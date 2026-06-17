async def signal(update, context):
    try:
        # ডাটা আনার সময় কিছুটা দেরি হতে পারে, তাই ব্যবহারকারীকে জানান
        await update.message.reply_text("🔎 মার্কেট ডাটা বিশ্লেষণ করছি, দয়া করে ১-২ সেকেন্ড অপেক্ষা করুন...")
        
        # EUR/USD এর ডাটা ফেচিং
        ticker = yf.Ticker("EURUSD=X")
        data = ticker.history(period="1d", interval="15m")
        
        if data.empty:
            await update.message.reply_text("দুঃখিত, বর্তমানে মার্কেটের ডাটা পাওয়া যাচ্ছে না।")
            return

        price = data['Close'].iloc[-1]
        
        # সিগন্যাল লজিক (আপনি আপনার মতো এখানে শর্ত বাড়াতে পারেন)
        signal_msg = (f"📊 লাইভ মার্কেট সিগন্যাল (EUR/USD)\n"
                      f"💵 বর্তমান প্রাইস: {price:.5f}\n"
                      f"🚀 পরামর্শ: বর্তমান মার্কেট ট্রেন্ড অনুযায়ী এন্ট্রি চেক করুন।\n"
                      f"⚠️ মনে রাখবেন: বটটি শুধুমাত্র তথ্যের জন্য।")
        
        await update.message.reply_text(signal_msg)
        
    except Exception as e:
        # যদি কোনো এরর হয়, তবে সেটি লগে বা টেলিগ্রামে দেখাবে
        await update.message.reply_text(f"এরর হয়েছে: {str(e)}")
