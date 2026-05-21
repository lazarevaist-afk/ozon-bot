from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# ===== TOKEN =====
TOKEN = os.getenv("TOKEN")

# ===== TELEGRAM BOT =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("бот жив")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))


# ===== FAKE WEB SERVER (для Render порта) =====
def run_web():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running")

    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


# ===== START EVERYTHING =====
if __name__ == "__main__":
    print("BOT STARTED")

    # запускаем веб-сервер в фоне
    threading.Thread(target=run_web, daemon=True).start()

    # запускаем telegram bot
    app.run_polling()
