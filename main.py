from flask import Flask
from threading import Thread
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from openai import OpenAI


# =========================
# KEEP ALIVE SERVER
# =========================
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "🤖 Jarvis Alive"

def run_web():
    app_web.run(host="0.0.0.0", port=8080)

Thread(target=run_web).start()


# =========================
# OPENAI CLIENT
# =========================
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# =========================
# TELEGRAM REPLY FUNCTION
# =========================
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Kamu adalah Jarvis AI assistant yang pintar dan ramah."},
            {"role": "user", "content": user_text}
        ]
    )

    await update.message.reply_text(
        response.choices[0].message.content
    )


# =========================
# TELEGRAM BOT START
# =========================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
)

print("🚀 Jarvis Online...")
app.run_polling()