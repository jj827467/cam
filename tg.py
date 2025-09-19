from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8375822827:AAHn8hSmurdScTzTUXp-wK7cxxgpI1TACaE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"你的 chat_id 是 {chat_id}")
    print("使用者 chat_id:", chat_id)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot 已啟動，請到 Telegram 發 /start 測試")
    app.run_polling()

if __name__ == "__main__":
    main()
