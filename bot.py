from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

TOKEN = os.getenv("TOKEN")
OWNER_ID = 8409916382


def allowed(user_id):
    return user_id == OWNER_ID


# ================= LEAD ENGINE =================
def generate_leads(query: str):

    # имитация реальных e-commerce сегментов
    base_sources = [
        "Wildberries seller",
        "Ozon store",
        "Shopify store",
        "Instagram shop",
        "Marketplace seller",
        "Local e-commerce brand"
    ]

    leads = []

    for source in base_sources:

        leads.append({
            "name": f"{query} - {source}",
            "weakness": [
                "нет инфографики",
                "слабые фото",
                "нет брендинга",
                "шаблонные карточки"
            ],
            "offer": f"""
💡 Оффер для {query}:

Я могу улучшить ваши карточки товаров и визуал на маркетплейсах.

📈 Это обычно даёт +15–40% к продажам.

У вас есть слабые точки:
- визуал
- упаковка
- позиционирование

Могу предложить аудит и редизайн карточек.
"""
        })

    return leads


# ================= TELEGRAM =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not allowed(update.effective_user.id):
        await update.message.reply_text("Доступ запрещён")
        return

    await update.message.reply_text(
        "Бот лидогенерации готов 🔥\n\n/search косметика"
    )


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not allowed(update.effective_user.id):
        await update.message.reply_text("Нет доступа")
        return

    query = " ".join(context.args)

    if not query:
        await update.message.reply_text("Пример:\n/search косметика")
        return

    leads = generate_leads(query)

    text = f"🔍 Найдено лидов: {len(leads)}\n\n"

    for l in leads:
        text += f"🏪 {l['name']}\n\n⚠️ Проблемы:\n- " + "\n- ".join(l["weakness"]) + "\n\n" + l["offer"] + "\n" + "-"*30 + "\n\n"

    await update.message.reply_text(text)


# ================= WEB SERVER =================
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
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("search", search))

if __name__ == "__main__":
    print("LEAD BOT V6 STARTED", flush=True)

    threading.Thread(target=run_web, daemon=True).start()

    app.run_polling()
