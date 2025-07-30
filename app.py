import time
import threading
from keep_alive import keep_alive
from linkedin_scraper import get_remote_jobs
from telegram_bot import send_to_telegram

def job_runner():
    while True:
        try:
            jobs = get_remote_jobs()
            for job in jobs:
                send_to_telegram(job)
        except Exception as e:
            print(f"Erro ao buscar ou enviar vagas: {e}")
        time.sleep(300)  # 5 minutos

keep_alive()
threading.Thread(target=job_runner).start()
