import telebot
from google.genai import Client
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- ЗАГЛУШКА ДЛЯ RENDER (чтобы он не ругался на порты) ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def keep_alive():
    # Render сам выдает нужный порт через переменную PORT
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

# Запускаем фейковый сервер в отдельном потоке, чтобы он не мешал боту
threading.Thread(target=keep_alive, daemon=True).start()
# ---------------------------------------------------------

# Твои ключи
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8643394823:AAEu6dFcZUF1S7EgfXyATp1j0G76fPAVWJM")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyA8_13BbZW8cROuFjbpaN25KEKIWvxvIEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
gemini_client = Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, Добрыня! 🚀\nЯ облачный Gemini-бот. Спрашивай что угодно!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=message.text
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка связи с ИИ. Попробуй позже.")
        print(f"Ошибка API: {e}")

if __name__ == "__main__":
    print("🤖 Бот запущен в штатном режиме!")
    bot.infinity_polling()
