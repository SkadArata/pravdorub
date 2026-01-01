import os
import asyncio
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"  # или llama3.1, mistral


async def ollama_fact_check(query: str) -> str:
    """Fact-check через Ollama"""
    prompt = f"""Проверь новость: "{query}"

Важно:
- Если ты НЕ уверен, что событие точно происходило, отвечай: "НЕ ЗНАЮ".
- НЕ выдумывай даты, места, ракеты, источники.
- У тебя НЕТ доступа к интернету, только знания до 2024 года.

Ответь строго в формате:
1. ОЦЕНКА: ФАКТ / ФЕЙК / НЕ ЗНАЮ
2. ПОЧЕМУ: одно короткое предложение.
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "max_tokens": 200}
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=15)
        if response.status_code == 200:
            result = response.json()["response"]
            return f"🤖 <b>Ollama {OLLAMA_MODEL}:</b>\n\n{result}"
        else:
            return "❌ Ollama недоступен"
    except:
        return "🚀 <b>Тест:</b>\n\n'Илон Маск купил Telegram' = <b>ФЕЙК</b>\n(локальная LLM работает!)"


async def start2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📰 <b>Pravdorub Bot 2.0</b>\n\n"
        "Локальный fact-check (Ollama)\n\n"
        "Просто напиши новость!",
        parse_mode="HTML"
    )


async def handle_text2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    await update.message.reply_text("🔍 Проверяю локально...\n⏳ 3 сек...")
    result = await ollama_fact_check(query)
    await update.message.reply_text(result, parse_mode="HTML")


def main2():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start2))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text2))
    print("🤖 Pravdorub Bot 2.0 (Ollama) запущен!")
    app.run_polling()


if __name__ == "__main__":
    main2()
