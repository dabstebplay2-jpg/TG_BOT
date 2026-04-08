import telebot
from google.genai import Client
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# 1. Заглушка для Render (чтобы не было ошибок порта)
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()

# 2. Настройка ключей (берем из настроек Render)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
G_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN)
client = Client(api_key=G_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я теперь работаю в облаке. Спрашивай!")

@bot.message_handler(func=lambda m: True)
def chat(message):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(message, "Произошла ошибка связи с ИИ.")

if __name__ == "__main__":
    bot.infinity_polling()
