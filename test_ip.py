import requests
import sys

print("--- СТАРТ ТЕСТА СЕТИ ---")

try:
    print("1. Пытаюсь достучаться до сервера проверки IP...")
    # Ставим timeout=10 секунд. Если за 10 сек ответа нет — значит сеть блокирует запрос.
    response = requests.get('https://ipapi.co/json/', timeout=10)
    
    print(f"2. Получен ответ! Статус-код: {response.status_code}")
    
    data = response.json()
    ip = data.get('ip')
    country = data.get('country_name')
    
    print(f"3. Твой текущий IP: {ip}")
    print(f"4. Страна по мнению сервера: {country}")
    
    if data.get('country') == 'RU':
        print("\n❌ ИТОГ: VPN не подхватился. Скрипты видят твой реальный IP (РФ).")
    else:
        print("\n✅ ИТОГ: VPN работает! Видна другая страна.")

except requests.exceptions.Timeout:
    print("\n❌ ОШИБКА: Время ожидания истекло. Похоже, твой VPN блокирует запросы от Python.")
except Exception as e:
    print(f"\n❌ ОШИБКА: {e}")

print("--- ТЕСТ ЗАВЕРШЕН ---")