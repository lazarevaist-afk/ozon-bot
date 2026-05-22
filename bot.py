from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# ================= TOKEN =================
TOKEN = os.getenv("TOKEN")

OWNER_ID = 8409916382


def allowed(user_id):
    return user_id == OWNER_ID


# ================= TELEGRAM HANDLERS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not allowed(update.effective_user.id):
        await update.message.reply_text("Доступ запрещён")
        return

    await update.message.reply_text(
        "Бот готов ✅\n\n/search детские товары"
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not allowed(update.effective_user.id):
        await update.message.reply_text("Нет доступа")
        return

    query = " ".join(context.args)

    if not query:
        await update.message.reply_text(
            "Пример:\n/search косметика"
        )
        return

    text = f"""
Поиск запущен 🔍

Категория:
{query}

Фильтры:

🇷🇺 только Россия
❌ исключить Китай

⭐ отзывы: 10–1000
📦 заказов: 1000–11000
🛍 товаров: 5–100

🏷 мини-бренды
🏭 OEM

📄 до 30 продавцов
🧠 антидубли 90 дней

⏳ подготовка поиска...
"""

    await update.message.reply_text(text)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))


# ================= FAKE SERVER (Render fix) =================
def run_web():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running")

    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()


# ================= START =================
if __name__ == "__main__":
    print("BOT STARTED", flush=True)

    # запускаем порт для Render
    threading.Thread(target=run_web, daemon=True).start()

    # запускаем Telegram bot
    app.run_polling()
