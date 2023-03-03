import requests
import json

# Define la URL de la vista que maneja las actualizaciones del bot
url = 'https://33b0-181-235-13-53.ngrok.io/webhooks/bot/'

# Define la URL del webhook del bot de Telegram
telegram_webhook_url = f'https://api.telegram.org/bot5997463720:AAG_WMB8BOoX97cRc5AE5bfwWZS9N3QFe60/setWebhook?url={url}'

otra_url = 'https://api.telegram.org/bot5997463720:AAG_WMB8BOoX97cRc5AE5bfwWZS9N3QFe60/setWebhook?url=https://33b0-181-235-13-53.ngrok.io/webhooks/bot/'

# Envía la solicitud POST al webhook del bot de Telegram
response = requests.post(telegram_webhook_url)

# Imprime la respuesta
print(json.loads(response.content))
json.loads(response.content)
