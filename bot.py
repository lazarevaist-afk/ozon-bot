from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


# ==========================
# TOKEN
# ==========================
TOKEN = os.getenv("TOKEN")


# ==========================
# /start
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
Бот поиска продавцов Ozon запущен ✅

Команды:

/search косметика
/search детские товары
/search товары для дома

/niche — список ниш
"""

    await update.message.reply_text(text)


# ==========================
# /search
# ==========================
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = " ".join(context.args)

    if not query:
        await update.message.reply_text(
            "Пример:\n/search косметика"
        )
        return

    response = f"""
Начинаю поиск в Ozon 🔍

Категория:
{query}

Фильтры:

✅ отзывы: 10–1000
✅ заказов магазина: 1000–11000
✅ товаров у продавца: от 5
✅ искать мини-бренды
✅ искать OEM
✅ искать карточки без инфографики

Статус:
🟡 тестовый режим

(следующим обновлением подключим реальный сбор результатов)
"""

    await update.message.reply_text(response)


# ==========================
# /niche
# ==========================
async def niche(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
Категории:

🧴 косметика
🧸 детские товары
🏠 товары для дома
🧼 уход
🧴 уход за волосами
🕯 свечи
🎁 подарки

Пример:

/search косметика
"""

    await update.message.reply_text(text)


# ==========================
# TELEGRAM
# ==========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("niche", niche))


# ==========================
# WEB SERVER (Render)
# ==========================
def run_web():

    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):

        def do_GET(self):

            self.send_response(200)
            self.end_headers()

            self.wfile.write(
                b"Bot is running"
            )

    server = HTTPServer(
        ("0.0.0.0", port),
        Handler
    )

    print(f"WEB STARTED {port}")

    server.serve_forever()


# ==========================
# START
# ==========================
if __name__ == "__main__":

    print("BOT STARTED")

    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    app.run_polling()
