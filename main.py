from flask import Flask
from openai import OpenAI
import os
import threading

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ======================
# CONFIG
# ======================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)

# ======================
# FLASK KEEP ALIVE (Railway)
# ======================

web = Flask(__name__)

@web.route("/")
def home():
    return "🤖 Jarvis AI Online"

def run_web():
    web.run(host="0.0.0.0", port=8080)

# ======================
# AI FUNCTION
# ======================

async def ai_response(text):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Kamu adalah Jarvis, AI assistant pribadi yang cerdas, cepat, dan membantu."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response.choices[0].message.content

# ======================
# TELEGRAM COMMANDS
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Jarvis Online!\nKetik apa saja untuk ngobrol."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Sistem berjalan normal.")

async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("Gunakan: /ai pertanyaan")
        return

    reply = await ai_response(text)
    await update.message.reply_text(reply)

# ======================
# CHAT LANGSUNG (NO COMMAND)
# ======================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    reply = await ai_response(text)

    await update.message.reply_text(reply)

# ======================
# MAIN PROGRAM
# ======================

if __name__ == "__main__":

    print("🚀 Starting Flask KeepAlive...")
    threading.Thread(target=run_web).start()

    print("🚀 Starting Telegram Bot...")

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("ai", ai_command))

    # CHAT BIASA = AI LANGSUNG
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("✅ Telegram Bot Running")

    app.run_polling()
