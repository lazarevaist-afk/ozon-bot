from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


# ===== TOKEN =====
TOKEN = os.getenv("TOKEN")


# ===== COMMAND /start =====
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


# ===== COMMAND /search =====
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = " ".join(context.args)

    if not query:
        await update.message.reply_text(
            "Напиши категорию.\n\nПример:\n/search косметика"
        )
        return

    result = f"""
Поиск запущен 🔍

Категория:
{query}

Фильтры:

✅ отзывы: 10–1000
✅ заказов магазина: 1000–11000
✅ товаров у продавца: от 5
✅ искать мини-бренды
✅ искать OEM
✅ искать карточки без инфографики

(сейчас работает тестовый режим)
"""

    await update.message.reply_text(result)


# ===== COMMAND /niche =====
async def niche(update: Update, context: ContextTypes.DEFAULT_TYPE):

    niches = """
Категории для поиска:

🧴 косметика
🧸 детские товары
🏠 товары для дома
🧼 уход
🕯 свечи
🧽 бытовые товары
🧴 уход за волосами
🎁 подарки

Пример:

/search косметика
"""

    await update.message.reply_text(niches)


# ===== TELEGRAM APP =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("niche", niche))


# ===== WEB SERVER FOR RENDER =====
def run_web():

    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):

        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running")

    server = HTTPServer(("0.0.0.0", port), Handler)

    print(f"WEB SERVER STARTED {port}")

    server.serve_forever()


# ===== START =====
if __name__ == "__main__":

    print("BOT STARTED")

    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    app.run_polling()
