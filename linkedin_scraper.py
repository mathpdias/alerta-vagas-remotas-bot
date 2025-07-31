import requests
from bs4 import BeautifulSoup
import re

def is_valid_job(title, location, description):
    # Verifica se a vaga é para o Brasil
    location_ok = "brasil" in location.lower() or "brazil" in location.lower()

    # Evita títulos/descrições que não possuem caracteres do português (útil para filtrar inglês puro)
    has_portuguese_chars = re.search(r"[à-úÀ-Ú]", title + description) is not None

    return location_ok and has_portuguese_chars

def get_remote_jobs():
    url = (
        "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/"
        "search?keywords=Remoto&location=Brasil&trk=public_jobs_jobs-search-bar_search-submit"
        "&position=1&pageNum=0&f_TPR=r86400&f_WT=2"
    )
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Erro ao buscar vagas:", e)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_elements = soup.find_all("li")

    jobs = []
    for job in job_elements:
        try:
            title = job.find("h3").get_text().strip()
            company = job.find("h4").get_text().strip()
            location = job.find("span", class_="job-search-card__location").text.strip()
            link = job.find("a")["href"].strip()

            if not link.startswith("https://www.linkedin.com"):
                continue

            description = f"{title} {company}"

            if is_valid_job(title, location, description):
                job_message = (
                    f"💼 *{title}*\n"
                    f"🏢 {company}\n"
                    f"📍 {location}\n"
                    f"🔗 {link}"
                )
                jobs.append(job_message)
        except AttributeError:
            continue

    return jobs
