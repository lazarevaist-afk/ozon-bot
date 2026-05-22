import os
import threading
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from db import init_db, add_seller, seller_exists

# ================= CONFIG =================
TOKEN = os.getenv("TOKEN")
OWNER_ID = 8409916382


def allowed(user_id: int) -> bool:
    return user_id == OWNER_ID


# ================= INIT DB =================
init_db()


# ================= SCRAPER (REAL Ozon light parsing) =================
def search_ozon(query: str):
    """
    Стабильный вариант без прокси:
    берём HTML выдачи Ozon и вытаскиваем товары
    """

    url = "https://www.ozon.ru/search/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    params = {"text": query}

    results = []

    try:
        r = requests.get(url, params=params, headers=headers, timeout=15)
        html = r.text

        # ищем ссылки на товары
        import re

        links = re.findall(r"/product/[^\"']+", html)

        seen = set()

        for link in links:
            full_link = "https://www.ozon.ru" + link

            if full_link in seen:
                continue

            seen.add(full_link)

            title = "Ozon product"
            seller = "Ozon seller"

            results.append({
                "title": title,
                "seller": seller,
                "link": full_link
            })

            if len(results) >= 30:
                break

    except Exception as e:
        print("SCRAPER ERROR:", e)

    return results


# ================= TELEGRAM =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not allowed(update.effective_user.id):
        return await update.message.reply_text("Доступ запрещён")

    await update.message.reply_text(
        "SAAS бот запущен 🔥\n\n/search косметика"
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not allowed(update.effective_user.id):
        return await update.message.reply_text("Нет доступа")

    query = " ".join(context.args)

    if not query:
        return await update.message.reply_text("Пример: /search косметика")

    data = search_ozon(query)

    if not data:
        return await update.message.reply_text("Ничего не найдено ❌")

    text = f"🔍 Найдено: {len(data)}\n\n"

    saved = 0

    for item in data:

        name = item["seller"]

        # антидубли 90 дней
        if seller_exists(name):
            continue

        add_seller(
            name=name,
            title=item["title"],
            link=item["link"],
            query=query
        )

        saved += 1

        text += (
            f"🏪 {name}\n"
            f"📦 {item['title']}\n"
            f"🔗 {item['link']}\n\n"
        )

    text += f"💾 Сохранено новых лидов: {saved}"

    await update.message.reply_text(text)


# ================= WEB SERVER (Render fix) =================
def run_web():
    port = int(os.environ.get("PORT", 10000))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running")

    HTTPServer(("0.0.0.0", port), Handler).serve_forever()


# ================= START =================
if __name__ == "__main__":
    print("SAAS V8 BOT STARTED", flush=True)

    threading.Thread(target=run_web, daemon=True).start()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))

    app.run_polling()
