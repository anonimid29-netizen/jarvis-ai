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
