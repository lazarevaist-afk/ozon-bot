from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

OWNER_ID = 8409916382


def allowed(user_id):
    return user_id == OWNER_ID


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

print("BOT STARTED")

app.run_polling()
