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
import os

port = int(os.environ.get("PORT", 10000))

from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

server = HTTPServer(("0.0.0.0", port), Handler)
server.serve_forever()
