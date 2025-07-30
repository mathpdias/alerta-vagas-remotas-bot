import time
import requests
from flask import Flask
import threading
from linkedin_scraper import get_remote_jobs  # importando a função correta

# --- CONFIGURAÇÕES ---
TOKEN = '8434789876:AAH0WXHNnYMGoIBhanpf4wpQyorqMqYPatU'
CANAL_ID = '-1002621159705'

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

# --- FILTROS ---
CARGOS_ACEITOS = [
    "assistente de suporte", "analista de suporte", "customer success", "sucesso do cliente",
    "assistente administrativo", "analista administrativo", "assistente de atendimento",
    "agente de atendimento", "atendimento digital", "assistente virtual", "virtual assistant",
    "gestão de relacionamento", "auxiliar administrativo", "suporte ao cliente", "suporte técnico",
    "assistente comercial", "assistente de vendas", "secretário", "secretária"
]

PALAVRAS_PROIBIDAS = [
    "customer support", "english", "bilingual", "remote usa", "home based in"
]

LOCAIS_BRASIL = [
    "brasil", "remoto", "são paulo", "rio de janeiro", "belo horizonte",
    "porto alegre", "curitiba", "recife", "salvador", "fortaleza", "campinas", "br"
]

# --- FUNÇÃO PRINCIPAL ---
def buscar_vagas():
    print("Verificando novas vagas...")
    try:
        vagas = get_remote_jobs()  # obtém vagas reais da API pública do LinkedIn

        for vaga in vagas:
            link = vaga['link']
            title = vaga['title'].lower()
            company = vaga['company']
            location = vaga['location'].lower()

            if link in historico_vagas:
                continue

            cargo_valido = any(c in title for c in CARGOS_ACEITOS)
            titulo_em_ingles = any(p in title for p in PALAVRAS_PROIBIDAS)
            vaga_no_brasil = any(p in location for p in LOCAIS_BRASIL) or "brazil" in link.lower()

            if cargo_valido and not titulo_em_ingles and vaga_no_brasil:
                mensagem = f"""📢 *Nova vaga encontrada!*

📌 *Título:* {vaga['title']}
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
