from flask import Flask
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@app.route("/")
def home():
    return "Jarvis AI Running 🚀"

@app.route("/ai")
def ai():
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":"buat konten facebook"}]
    )
    return response.choices[0].message.content

app.run(host="0.0.0.0", port=8080)

import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# ======================
# AI RESPONSE
# ======================
async def ai_response(text):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Kamu adalah Jarvis, AI assistant pribadi yang cerdas, cepat dan membantu."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

# ======================
# COMMANDS
# ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Jarvis Online.\nKetik /help")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
Perintah Jarvis:
/ai [pertanyaan]
/status
""")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Sistem AI berjalan normal.")

async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)

    if not text:
        await update.message.reply_text("Tulis pertanyaan setelah /ai")
        return

    reply = await ai_response(text)
    await update.message.reply_text(reply)

# ======================
# MAIN
# ======================

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("ai", ai_command))

app.run_polling()
