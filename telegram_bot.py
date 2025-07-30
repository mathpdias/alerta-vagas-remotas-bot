import requests
import os

BOT_TOKEN = os.getenv("8070777170:AAEXhz786u288fZGkTEvElSjDwm2jz0f-pk")
CHAT_ID = os.getenv("-1002311325037")

sent_jobs = set()

def send_to_telegram(message):
    if message in sent_jobs:
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)
    sent_jobs.add(message)
