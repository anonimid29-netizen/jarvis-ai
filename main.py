from flask import Flask
from openai import OpenAI
import os
import threading

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ======================
# CONFIG
# ======================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)

# ======================
# FLASK SERVER (Railway keep alive)
# ======================

web = Flask(__name__)

@web.route("/")
def home():
    return "🤖 Jarvis AI Online"

# ======================
# AI FUNCTION
# ======================

async def ai_response(text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content":"Kamu adalah Jarvis, AI assistant pribadi yang pintar dan cepat."},
            {"role":"user","content":text}
        ]
    )
    return response.choices[0].message.content

# ======================
# TELEGRAM COMMANDS
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Jarvis Online!")

async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("Gunakan: /ai pertanyaan")
        return

    reply = await ai_response(text)
    await update.message.reply_text(reply)

# ======================
# TELEGRAM BOT RUNNER
# ======================

def run_telegram():
    bot = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("ai", ai_command))

    bot.run_polling()

# ======================
# START BOTH SYSTEMS
# ======================

if __name__ == "__main__":
    threading.Thread(target=run_telegram).start()
    web.run(host="0.0.0.0", port=8080)
