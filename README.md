# Gupy Job Scraper — Coleta Distribuída + Histórico de Vagas

Este projeto implementa um coletor avançado de vagas da Gupy utilizando **Playwright**, **Python** e **Streamlit**, com suporte a **histórico incremental**, detecção de vagas novas/removidas e análise interativa.

---

## 🚀 Visão Geral

A Gupy deixou de expor vagas via API, JSON ou DOM no portal global (`portal.gupy.io`).  
Para contornar isso, este projeto coleta vagas diretamente das **páginas individuais das empresas**, que ainda possuem HTML acessível.

A solução inclui:

- Coleta automatizada de vagas em **70 empresas** que utilizam Gupy.
- Extração estruturada de:
  - Título  
  - Empresa  
  - Cidade  
  - Estado  
  - Modalidade  
  - URL  
- Histórico incremental com detecção de:
  - `nova`
  - `ativa`
  - `removida`
- Dashboard em Streamlit para análise e exportação.

---

## 🧩 Arquitetura

### 1. Coletor (Playwright)
O arquivo `coletar_vagas.py` percorre uma lista de empresas e extrai vagas diretamente do HTML:

- Acessa `https://<empresa>.gupy.io/`
- Localiza elementos `a[data-testid="job-card"]`
- Extrai campos estruturados
- Salva a coleta atual em `vagas.csv`

### 2. Histórico de Vagas
O coletor compara `vagas.csv` com `vagas_historico.csv`:

- Marca vagas novas
- Atualiza vagas ativas
- Identifica vagas removidas
- Mantém datas de primeira e última aparição

### 3. Dashboard (Streamlit)
O arquivo `app.py` permite:

- Filtrar por cargo, modalidade, estado e status
- Visualizar histórico completo
- Exportar CSV filtrado

---

## 🛠️ Tecnologias Utilizadas

- Python 3.10  
- Playwright  
- Pandas  
- Streamlit  
- CSV incremental  

---

## ▶️ Como executar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
playwright install

2. Rodar o coletor
python coletar_vagas.py

3. Rodar o dashboard
streamlit run app.py

📁 Estrutura do Projeto
├── coletar_vagas.py
├── app.py
├── vagas.csv
├── vagas_historico.csv
└── README.md

Observações
O coletor funciona apenas com Python 3.10 devido a limitações do Playwright no Windows.

A lista de empresas pode ser expandida facilmente.

O histórico é atualizado automaticamente a cada execução.

📜 Licença
MIT License.

🤝 Contribuições
Pull requests são bem-vindos!
Sinta-se à vontade para sugerir novas empresas, melhorias no parser ou novas funcionalidades.
