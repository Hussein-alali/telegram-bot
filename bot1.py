import aiofiles
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- إعدادات البوت ---
TOKEN = "8130116223:AAE897LRPcxnSHAWkxu2lbhH0bstrIgEmag"  # استبدل هذا بالتوكن الخاص بك

# قائمة الفيديوهات المخزنة محليًا على الخادم
VIDEO_FILES = {
    "الصف 12": {
        "فيديو 1": r"C:\Users\dell\Desktop\Bot\12\1.mp4",
        "فيديو 2": r"C:\Users\dell\Desktop\Bot\12\2.mp4",
    },
    "الصف 11": {
        "فيديو 1": r"C:\Users\dell\Desktop\Bot\11\1.mp4",
        "فيديو 2": r"C:\Users\dell\Desktop\Bot\11\2.mp4",
    },
    "الصف 10": {
        "فيديو 1": r"C:\Users\dell\Desktop\Bot\10\1.mp4",
        "فيديو 2": r"C:\Users\dell\Desktop\Bot\10\2.mp4",
    }
}

# تخزين الصف المحدد لكل مستخدم
user_selected_class = {}

# --- وظائف البوت ---

# عرض لوحة المفاتيح الرئيسية عند بدء التشغيل
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["الصف 12"],
        ["أمتحانات سابقة", "المنهج"],
        ["الصف 11"],
        ["أمتحانات سابقة", "المنهج"],
        ["الصف 10"],
        ["أمتحانات سابقة", "المنهج"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("📚 اختر الصف الذي تريده:", reply_markup=reply_markup)

# التعامل مع ردود المستخدم عند الضغط على الأزرار
async def handle_reply_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text in ["الصف 12", "الصف 11", "الصف 10"]:
        user_selected_class[user_id] = text
        await update.message.reply_text(f"📘 لقد اخترت {text}، ماذا تريد؟")

    elif text == "أمتحانات سابقة":
        await update.message.reply_text("📝 هنا ستجد الامتحانات السابقة!")

    elif text == "المنهج":
        if user_id in user_selected_class:
            selected_class = user_selected_class[user_id]
            keyboard = [[video] for video in VIDEO_FILES[selected_class].keys()]
            keyboard.append(["⬅️ رجوع"])  # زر الرجوع إلى القائمة الرئيسية
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(f"🎥 اختر فيديو من منهج {selected_class}:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("⚠️ الرجاء اختيار صف أولاً قبل عرض المنهج.")

    elif text in ["فيديو 1", "فيديو 2"]:
        if user_id in user_selected_class:
            selected_class = user_selected_class[user_id]
            video_path = VIDEO_FILES[selected_class].get(text)
            if video_path:
                try:
                    async with aiofiles.open(video_path, "rb") as video_file:
                        video_data = await video_file.read()
                    await update.message.reply_video(video=video_data, caption=f"📹 {text} من {selected_class}")
                except Exception as e:
                    await update.message.reply_text(f"⚠️ خطأ في تحميل الفيديو: {str(e)}")
            else:
                await update.message.reply_text("⚠️ الفيديو غير متوفر حالياً.")
        else:
            await update.message.reply_text("⚠️ الرجاء اختيار صف أولاً قبل مشاهدة الفيديوهات.")

    elif text == "⬅️ رجوع":
        await start(update, context)  # إعادة عرض القائمة الرئيسية

    else:
        await update.message.reply_text("⚠️ اختيار غير متاح، الرجاء اختيار أحد الأزرار.")

# --- تشغيل البوت ---
def main():
    application = Application.builder().token(TOKEN).build()

    # الأوامر والردود
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply_keyboard))

    # تشغيل البوت
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True, timeout=10)

if __name__ == "__main__":
    main()