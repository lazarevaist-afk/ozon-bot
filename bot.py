from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("бот жив")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    print("BOT STARTED")
    app.run_polling()
