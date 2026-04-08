import telebot
from google.genai import Client
import os

# 1. Забираем ключи из защищенных переменных окружения (это стандарт безопасности)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "8643394823:AAEu6dFcZUF1S7EgfXyATp1j0G76fPAVWJM")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyA8_13BbZW8cROuFjbpaN25KEKIWvxvIEY")

# 2. Инициализация
bot = telebot.TeleBot(TELEGRAM_TOKEN)
gemini_client = Client(api_key=GEMINI_API_KEY)

# 3. Обработка команд
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "Привет, Добрыня! 🚀\n"
        "Я обновленный Gemini-бот. Теперь я живу в облаке и работаю без перебоев.\n"
        "Спрашивай что угодно!"
    )
    bot.reply_to(message, welcome_text)

# 4. Обработка сообщений с ИИ
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Прямой запрос к Gemini (в облаке блокировок нет)
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=message.text
        )
        bot.reply_to(message, response.text)
        
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка связи с ИИ. Попробуй позже.")
        print(f"Ошибка API: {e}")

# 5. Запуск
if __name__ == "__main__":
    print("🤖 Бот запущен в штатном режиме!")
    bot.infinity_polling()