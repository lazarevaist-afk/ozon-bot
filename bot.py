from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import json

# ================= TOKEN =================
TOKEN = os.getenv("TOKEN")

OWNER_ID = 8409916382


def allowed(user_id):
    return user_id == OWNER_ID


# ================= Ozon parser (FIXED) =================
def search_ozon_sellers(query: str):
    url = "https://www.ozon.ru/api/composer-api.bx/page/json/v2"

    params = {
        "url": f"/search/?text={query}"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)
        data = r.json()
    except Exception as e:
        print("REQUEST ERROR:", e)
        return []

    sellers = []
    seen = set()

    try:
        widgets = data.get("widgetStates", {})

        for key, value in widgets.items():

            if "searchResultsV2" in key or "searchResults" in key:

                try:
                    parsed = json.loads(value)
                except:
                    continue

                items = parsed.get("items", [])

                for item in items:

                    seller = (
                        item.get("seller", {}).get("name")
                        or item.get("brand", {}).get("name")
                    )

                    title = item.get("title")

                    product_id = (
                        item.get("action", {}).get("id")
                        or item.get("id")
                    )

                    if not seller or not product_id:
                        continue

                    if seller in seen:
                        continue

                    seen.add(seller)

                    link = f"https://www.ozon.ru/product/{product_id}"

                    sellers.append({
                        "seller": seller,
                        "title": title,
                        "link": link
                    })

                    if len(sellers) >= 30:
                        return sellers

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
        await update.message.reply_text("Ничего не найдено")
        return

    text = f"🔍 Найдено продавцов: {len(sellers)}\n\n"

    for s in sellers:
        text += f"🏪 {s['seller']}\n📦 {s['title']}\n🔗 {s['link']}\n\n"

    await update.message.reply_text(text)


# ================= BOT =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))


# ================= RENDER PORT FIX =================
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
