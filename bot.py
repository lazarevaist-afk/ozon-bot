from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import re

# ================= TOKEN =================
TOKEN = os.getenv("TOKEN")

OWNER_ID = 8409916382


def allowed(user_id):
    return user_id == OWNER_ID


# ================= Ozon HTML parser =================
def search_ozon_sellers(query: str):
    url = f"https://www.ozon.ru/search/?text={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=15)
        html = r.text
    except Exception as e:
        print("REQUEST ERROR:", e)
        return []

    sellers = []
    seen = set()

    try:
        # ищем блоки продавцов в HTML (грубый, но стабильный вариант)
        blocks = re.findall(r'"seller"\s*:\s*{.*?}', html)

        for b in blocks:
            name_match = re.search(r'"name"\s*:\s*"([^"]+)"', b)

            if not name_match:
                continue

            seller = name_match.group(1)

            if seller in seen:
                continue

            seen.add(seller)

            sellers.append({
                "seller": seller,
                "title": "Ozon product",
                "link": url
            })

            if len(sellers) >= 30:
                break

    except Exception as e:
        print("PARSE ERROR:", e)

    return sellers


# ================= TELEGRAM =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not allowed(update.effective_user.id):
        await update.message.reply_text("Доступ запрещён")
        return

    await update.message.reply_text("Бот готов ✅\n\n/search косметика")


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not allowed(update.effective_user.id):
        await update.message.reply_text("Нет доступа")
        return

    query = " ".join(context.args)

    if not query:
        await update.message.reply_text("Пример:\n/search товары для дома")
        return

    sellers = search_ozon_sellers(query)

    if not sellers:
        await update.message.reply_text("Ничего не найдено (Ozon ограничил выдачу)")
        return

    text = f"🔍 Найдено продавцов: {len(sellers)}\n\n"

    for s in sellers:
        text += f"🏪 {s['seller']}\n📦 {s['title']}\n🔗 {s['link']}\n\n"

    await update.message.reply_text(text)


# ================= BOT =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))


# ================= RENDER WEB SERVER =================
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

    threading.Thread(target=run_web, daemon=True).start()

    app.run_polling()
