import time
import requests
from bs4 import BeautifulSoup
from flask import Flask
import threading

# --- CONFIGURAÇÕES ---
TOKEN = '8434789876:AAH0WXHNnYMGoIBhanpf4wpQyorqMqYPatU'
CANAL_ID = '-1002621159705'
URL = 'https://www.linkedin.com/jobs/search/?f_WT=2&geoId=100454369&keywords=remoto&location=Brasil&sortBy=R'
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# --- FLASK KEEP-ALIVE ---
app = Flask('')

@app.route('/')
def home():
    return "Bot ativo."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# --- HISTÓRICO ---
historico_vagas = []

# --- FUNÇÃO PRINCIPAL ---
def buscar_vagas():
    print("Verificando novas vagas...")
    try:
        response = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        vagas = soup.find_all('a', {'class': 'base-card__full-link'})

        for vaga in vagas:
            link = vaga['href']
            if link in historico_vagas:
                continue

            titulo = vaga.find('h3', {'class': 'base-search-card__title'})
            empresa = vaga.find('h4', {'class': 'base-search-card__subtitle'})
            local = vaga.find('span', {'class': 'job-search-card__location'})

            if not titulo or not empresa or not local:
                continue

            title = titulo.text.strip()
            company = empresa.text.strip()
            location = local.text.strip().lower()

            # --- CARGOS ACEITOS ---
            cargos_aceitos = [
                "assistente de suporte", "analista de suporte", "customer success", "sucesso do cliente",
                "assistente administrativo", "analista administrativo", "assistente de atendimento",
                "agente de atendimento", "atendimento digital", "assistente virtual", "virtual assistant",
                "gestão de relacionamento", "auxiliar administrativo", "suporte ao cliente", "suporte técnico",
                "assistente comercial", "assistente de vendas", "secretário", "secretária"
            ]

            # --- FILTRO CARGO ---
            cargo_valido = any(c in title.lower() for c in cargos_aceitos)

            # --- ELIMINA VAGAS EM INGLÊS OU ESTRANGEIRAS ---
            titulo_em_ingles = any(p in title.lower() for p in [
                "customer support", "english", "bilingual", "remote usa", "home based in"
            ])

            vaga_no_brasil = any(p in location for p in [
                "brasil", "remoto", "são paulo", "rio de janeiro", "belo horizonte",
                "porto alegre", "curitiba", "recife", "salvador", "fortaleza", "campinas", "br"
            ]) or "brazil" in link.lower()

            if cargo_valido and not titulo_em_ingles and vaga_no_brasil:
                mensagem = f"""📢 *Nova vaga encontrada!*

📌 *Título:* {title}
🏢 *Empresa:* {company}
📍 *Local:* {location.title()}
🔗 [Ver vaga]({link})"""

                enviar_telegram(mensagem)
                historico_vagas.append(link)

                if len(historico_vagas) > 100:
                    historico_vagas.pop(0)

    except Exception as e:
        print(f"Erro ao buscar vagas: {e}")

# --- TELEGRAM ---
def enviar_telegram(mensagem):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            'chat_id': CANAL_ID,
            'text': mensagem,
            'parse_mode': 'Markdown'
        }
        r = requests.post(url, data=payload)
        print("Mensagem enviada!", r.status_code)
    except Exception as e:
        print("Erro ao enviar:", e)

# --- LOOP ---
def iniciar_bot():
    while True:
        buscar_vagas()
        time.sleep(360)  # a cada 6 minutos

# --- EXECUÇÃO FINAL ---
keep_alive()
iniciar_bot()
