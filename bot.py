import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")


# ---------------- BOT ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает ✅")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    await update.message.reply_text(f"Ищу: {query}")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))


# ---------------- WEB SERVER (ВАЖНО ДЛЯ RENDER) ----------------

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")


def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


# запускаем веб-сервер в фоне
threading.Thread(target=run_web, daemon=True).start()


# ---------------- START BOT ----------------

if __name__ == "__main__":
    print("Bot started")
    app.run_polling()
