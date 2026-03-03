import time
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright

EMPRESAS = [
    "nubank", "vivo", "itau-unibanco", "ambev", "santander", "bradesco",
    "bancointer", "localiza", "bancopan", "magazineluiza", "stone", "c6bank",
    "via", "safra", "porto", "sulamerica", "raizen", "petlove", "totvs",
    "grupoboticario", "ambevtech", "arcelormittal", "bayer", "bosch",
    "brf", "cargill", "cielo", "cognizant", "dasa", "dell", "eletrobras",
    "energisa", "gerdau", "globo", "gol", "grendene", "grupoabril",
    "grupodimed", "grupofleury", "grupopaoacucar", "havan", "hospitalalemaooswaldocruz",
    "hospitalmoinhos", "ibm", "jbs", "johnsonandjohnson", "kroton", "loggi",
    "marisa", "mercadopago", "mercadolivre", "mrv", "nestle", "pagseguro",
    "petrobras", "prati-donaduzzi", "randstad", "renner", "rihappy",
    "sadia", "samsung", "senior", "serasa", "sicoob", "sodexo",
    "unimedbh", "vale", "weg", "whirlpool", "yduqs"
]


def coletar_vagas():
    dados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for slug in EMPRESAS:
            url = f"https://{slug}.gupy.io/"
            print(f"\nColetando vagas de: {url}")

            try:
                page.goto(url, timeout=30000)
                time.sleep(2)

                cards = page.locator("a[data-testid='job-card']")
                count = cards.count()

                print(f"Encontradas {count} vagas em {slug}")

                for i in range(count):
                    card = cards.nth(i)

                    titulo = card.locator("h2").inner_text(timeout=2000)
                    local = card.locator("span").nth(0).inner_text(timeout=2000)
                    modelo = card.locator("span").nth(1).inner_text(timeout=2000)
                    link = card.get_attribute("href")

                    cidade = ""
                    estado = ""

                    if "-" in local:
                        partes = local.split("-")
                        cidade = partes[0].strip()
                        estado = partes[1].strip()

                    dados.append({
                        "Título": titulo,
                        "Empresa": slug,
                        "Cidade": cidade,
                        "Estado": estado,
                        "Modelo": modelo,
                        "URL": link
                    })

            except Exception as e:
                print(f"Erro ao coletar {slug}: {e}")
                continue

        browser.close()

    df_atual = pd.DataFrame(dados)
    df_atual.to_csv("vagas.csv", index=False, encoding="utf-8-sig")

    print("\nAtualizando histórico...")

    try:
        df_hist = pd.read_csv("vagas_historico.csv")
    except FileNotFoundError:
        df_hist = pd.DataFrame()

    hoje = datetime.now().strftime("%Y-%m-%d")

    if df_hist.empty:
        df_atual["status"] = "nova"
        df_atual["data_primeira_vez"] = hoje
        df_atual["data_ultima_vez"] = hoje
        df_atual.to_csv("vagas_historico.csv", index=False, encoding="utf-8-sig")
        print("Histórico criado.")
        return

    df_hist["status"] = "removida"

    for _, vaga in df_atual.iterrows():
        mask = df_hist["URL"] == vaga["URL"]

        if mask.any():
            df_hist.loc[mask, "status"] = "ativa"
            df_hist.loc[mask, "data_ultima_vez"] = hoje
        else:
            nova = vaga.to_dict()
            nova["status"] = "nova"
            nova["data_primeira_vez"] = hoje
            nova["data_ultima_vez"] = hoje
            df_hist = pd.concat([df_hist, pd.DataFrame([nova])], ignore_index=True)

    df_hist.to_csv("vagas_historico.csv", index=False, encoding="utf-8-sig")
    print("Histórico atualizado com sucesso!")


if __name__ == "__main__":
    coletar_vagas()
