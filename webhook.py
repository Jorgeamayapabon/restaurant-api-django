import requests
import json

# Define la URL de la vista que maneja las actualizaciones del bot
# url = 'https://127.0.0.1:8000/telegram_webhook/'

# Define la URL del webhook del bot de Telegram
url = 'https://api.telegram.org/bot5997463720:AAG_WMB8BOoX97cRc5AE5bfwWZS9N3QFe60/setWebhook'
payload = {'url': 'https://c41c-201-228-214-44.ngrok.io/telegram_webhook/'}

response = requests.post(url, data=payload)
print(response.json())