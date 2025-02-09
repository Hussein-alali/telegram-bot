import aiofiles
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Bot Settings ---
TOKEN = "YOUR_BOT_TOKEN"  # Replace this with your bot token

# List of locally stored videos on the server
VIDEO_FILES = {
    "Grade 12": {
        "Video 1": r"C:\Users\dell\Desktop\Bot\12\1.mp4",
        "Video 2": r"C:\Users\dell\Desktop\Bot\12\2.mp4",
    },
    "Grade 11": {
        "Video 1": r"C:\Users\dell\Desktop\Bot\11\1.mp4",
        "Video 2": r"C:\Users\dell\Desktop\Bot\11\2.mp4",
    },
    "Grade 10": {
        "Video 1": r"C:\Users\dell\Desktop\Bot\10\1.mp4",
        "Video 2": r"C:\Users\dell\Desktop\Bot\10\2.mp4",
    }
}

# Store the selected grade for each user
user_selected_class = {}

# --- Bot Functions ---

# Display the main keyboard when the bot starts
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Grade 12"],
        ["Previous Exams", "Curriculum"],
        ["Grade 11"],
        ["Previous Exams", "Curriculum"],
        ["Grade 10"],
        ["Previous Exams", "Curriculum"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("📚 Select the grade you want:", reply_markup=reply_markup)

# Handle user responses when clicking buttons
async def handle_reply_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text in ["Grade 12", "Grade 11", "Grade 10"]:
        user_selected_class[user_id] = text
        await update.message.reply_text(f"📘 You have selected {text}, what do you want?")

    elif text == "Previous Exams":
        await update.message.reply_text("📝 Here you will find previous exams!")

    elif text == "Curriculum":
        if user_id in user_selected_class:
            selected_class = user_selected_class[user_id]
            keyboard = [[video] for video in VIDEO_FILES[selected_class].keys()]
            keyboard.append(["⬅️ Back"])  # Button to return to the main menu
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(f"🎥 Select a video from the {selected_class} curriculum:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("⚠️ Please select a grade first before viewing the curriculum.")

    elif text in ["Video 1", "Video 2"]:
        if user_id in user_selected_class:
            selected_class = user_selected_class[user_id]
            video_path = VIDEO_FILES[selected_class].get(text)
            if video_path:
                try:
                    async with aiofiles.open(video_path, "rb") as video_file:
                        video_data = await video_file.read()
                    await update.message.reply_video(video=video_data, caption=f"📹 {text} from {selected_class}")
                except Exception as e:
                    await update.message.reply_text(f"⚠️ Error loading video: {str(e)}")
            else:
                await update.message.reply_text("⚠️ The video is not available at the moment.")
        else:
            await update.message.reply_text("⚠️ Please select a grade first before watching videos.")

    elif text == "⬅️ Back":
        await start(update, context)  # Redisplay the main menu

    else:
        await update.message.reply_text("⚠️ Invalid selection, please choose one of the available options.")

# --- Run the Bot ---
def main():
    application = Application.builder().token(TOKEN).build()

    # Commands and responses
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply_keyboard))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True, timeout=10)

if __name__ == "__main__":
    main()
