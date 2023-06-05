import requests
import json

# Define la URL de la vista que maneja las actualizaciones del bot
url = 'https://cc1f-201-228-214-44.ngrok-free.app'

# Define la URL del webhook del bot de Telegram
telegram_webhook_url = f'https://api.telegram.org/bot5997463720:AAG_WMB8BOoX97cRc5AE5bfwWZS9N3QFe60/setWebhook?url={url}'
ngrok_url = 'https://a354-186-169-216-111.ngrok.io'
otra_url = 'https://api.telegram.org/bot5997463720:AAG_WMB8BOoX97cRc5AE5bfwWZS9N3QFe60/setWebhook?url=https://cc1f-201-228-214-44.ngrok-free.app/webhooks/bot/'

# Envía la solicitud POST al webhook del bot de Telegram
response = requests.post(telegram_webhook_url)

# Imprime la respuesta
print(json.loads(response.content))
json.loads(response.content)
