# bot3.py
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from news_handler3 import analyze_news3
from link_parser import extract_article  # твой парсер статьи [file:22]
import hashlib

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

##

MOZHNO_FILE = "mozhno.txt"


def save_user(update: Update) -> None:
    """Сохраняет user_id и имя в текстовый файл (без БД)."""
    user = update.effective_user  # telegram.User [web:153]
    user_id = user.id
    username = user.username or ""
    first_name = user.first_name or ""
    last_name = user.last_name or ""

###    line = f"{user_id};{username};{first_name};{last_name}\n"
###    line = f"{user_id}\n"
    anon_id = hashlib.sha256(str(user_id).encode("utf-8")).hexdigest()
    line = f"{anon_id}\n"

    try:
        # режим 'a' — дописать в конец файла, не стирая существующее [web:154][web:157]
        with open(MOZHNO_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        print(f"⚠ Ошибка записи в {MOZHNO_FILE}: {e}")


##

async def start3(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # сохранение id юзера при первом /start
    save_user(update)

    await update.message.reply_text(
        "📰 <b>Pravdorub Bot (ProxyAPI)</b>\n\n"
        "Ассистент по разбору новостей и проверке фейков с веб‑поиском.\n\n"
        "<b>Команды:</b>\n"
        "/news — анализ новости или утверждения\n\n"
        "<b>Просто напишите:</b> текст новости или отправьте ссылку на статью,\n"
        "а бот проверит факты и числа.",
        parse_mode="HTML",
    )


async def news3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 Напишите новость, утверждение или ссылку после /news"
    )


async def handle_text3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    # Примитивная проверка на URL
    if query.startswith(("http://", "https://")):
        await update.message.reply_text(
            "🌐 Вижу ссылку, парсю статью...\n⏳ 2–3 сек..."
        )
        extracted = await extract_article(query)
        # Для модели даём и ссылку, и извлечённый текст
        text_for_check = f"Новость по ссылке {query}:\n\n{extracted}"
    else:
        text_for_check = query

    print(f"🚀 [ProxyAPI] Анализирую: '{text_for_check[:100]}'")

    await update.message.reply_text(
        f"🔍 Анализирую через GPT (ProxyAPI): {text_for_check[:50]}...\n⏳ 2–3 сек..."
    )

    result = await analyze_news3(text_for_check)
    await update.message.reply_text(result, parse_mode="HTML")


def main3():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN не задан в .env")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start3))
    app.add_handler(CommandHandler("news", news3))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text3))

    print("🤖 Pravdorub Bot (ProxyAPI, GPT) запущен!")
    app.run_polling()


if __name__ == "__main__":
    main3()
