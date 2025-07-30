import requests

BOT_TOKEN = "8070777170:AAEXhz786u288fZGkTEvElSjDwm2jz0f-pk"
CHAT_ID = "-1002311325037"

def send_to_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    print("STATUS:", response.status_code)
    print("RESPOSTA:", response.text)

send_to_telegram("✅ Teste direto pelo Railway!")
