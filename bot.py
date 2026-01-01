import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from news_handler import analyze_news

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📰 <b>Pravdorub Bot</b>\n\n"
        "Проверяет достоверность источников\n\n"
        "<b>Команды:</b>\n"
        "/news — анализ новости\n"
        "/history — последние запросы\n\n"
        "<b>Inline:</b> @pravdorbot новость...\n\n"
        "<b>Просто напиши:</b> текст новости",
        parse_mode="HTML"
    )


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Напиши новость или ссылку после /news")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    print(f"🚀 Анализирую: '{query}'")

    await update.message.reply_text(f"🔍 Анализирую: {query[:50]}...\n⏳ 1 сек...")
    result = await analyze_news(query)
    await update.message.reply_text(result, parse_mode="HTML")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("🤖 Pravdorub Bot запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
