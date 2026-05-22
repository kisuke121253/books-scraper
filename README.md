# 📚 Books Scraper — RPA & AI

Automação de scraping desenvolvida em Python utilizando **Playwright**, **Pydantic** e integração com IA via **Groq (Llama 3)** para enriquecimento inteligente de dados.

O projeto realiza coleta automatizada de livros do site [Books to Scrape](https://books.toscrape.com?utm_source=chatgpt.com), exportando os resultados em JSON e CSV, com suporte opcional a enriquecimento semântico utilizando LLM.

---

# 🚀 Tecnologias Utilizadas

* Python 3.11+
* Playwright
* Pydantic
* Typer (CLI)
* Pytest
* Docker & Docker Compose
* Groq API
* PostgreSQL (opcional)

---

# 📦 Funcionalidades

* Scraping automatizado com Playwright
* Navegação headless
* Busca por categoria
* Busca por título específico
* Exportação para JSON e CSV
* Validação de dados com Pydantic
* Enriquecimento via IA usando Llama 3
* Ambiente Dockerizado
* Testes automatizados

---

# 📁 Estrutura do Projeto

```text
books-scraper/
├── docker-compose.yml
├── Dockerfile
├── main.py
├── README.md
├── requirements.txt
│
├── output/
│   ├── books.json
│   └── books.csv
│
├── scraper/
│   ├── ai_enrichment.py
│   ├── crawler.py
│   ├── models.py
│   ├── pipeline.py
│   ├── storage.py
│   └── __init__.py
│
├── tests/
│   ├── pytest.ini
│   ├── test_ai.py
│   ├── test_crawler.py
│   ├── test_pipeline.py
│   ├── test_storage.py
│   └── __init__.py
│
└── venv/
```

---

# ⚙️ Pré-requisitos

Antes de começar, certifique-se de possuir instalado:

* Python 3.11 ou superior
* Git
* Docker e Docker Compose (opcional)
* Navegador Chromium do Playwright

---

# 🔧 Instalação Local

## 1. Clone o repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd books-scraper
```

---

## 2. Crie o ambiente virtual

### Linux/macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 4. Instale o Chromium do Playwright

```bash
playwright install chromium
```

---

# 🔐 Configuração das Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto:

```env
# =========================
# GROQ API
# =========================

# Chave da API obtida em:
# https://console.groq.com
GROQ_API_KEY=gsk_sua_chave_aqui

# Modelo utilizado para enriquecimento
AI_MODEL=llama3-8b-8192

# =========================
# DATABASE (Opcional)
# =========================

DATABASE_URL=postgresql://postgres:postgres@db:5432/books
```

---

# 🤖 Fluxo de Enriquecimento com IA

Quando a flag `--ai` é utilizada, o sistema executa o seguinte fluxo:

1. O Playwright acessa a página do livro.
2. O scraper captura a descrição do produto.
3. O módulo `ai_enrichment.py` envia o texto para a API da Groq.
4. O modelo `llama3-8b-8192` processa o conteúdo.
5. A IA retorna um JSON estruturado contendo:

   * `theme`
   * `target_audience`
   * `short_summary`
6. O Pydantic valida os dados.
7. Os resultados são persistidos em:

   * `books.json`
   * `books.csv`

---

# 🖥️ Como Executar

## Execução básica

```bash
python main.py
```

---

# 🧠 Comandos Disponíveis

| Comando              | Descrição                   |
| -------------------- | --------------------------- |
| `--max-pages` / `-p` | Limita o número de páginas  |
| `--category` / `-c`  | Filtra por categoria        |
| `--search` / `-s`    | Busca por título específico |
| `--ai`               | Ativa enriquecimento via IA |
| `--verbose` / `-v`   | Exibe logs detalhados       |

---

# 📌 Exemplos de Uso

## Buscar livro específico

```bash
python main.py -s "It's Only the Himalayas"
```

---

## Limitar páginas

```bash
python main.py -p 2
```

---

## Filtrar categoria

```bash
python main.py -c travel_2
```

---

## Ativar IA

```bash
python main.py --ai
```

---

## Execução completa

```bash
python main.py --ai -s "It's Only the Himalayas" -p 1 -v
```

---

# 🐳 Docker

O projeto possui suporte completo a Docker.

---

## Build e execução

```bash
docker compose up --build
```

---

## Execução em background

```bash
docker compose up -d
```

---

## Derrubar containers

```bash
docker compose down
```

---

# 🏗️ Arquitetura Docker

O ambiente utiliza:

* `Dockerfile`
* `docker-compose.yml`
* Estratégia multi-stage build
* PostgreSQL opcional

A estrutura garante:

* Ambiente padronizado
* Isolamento de dependências
* Compatibilidade com Playwright
* Facilidade de deploy

---

# 🧪 Testes Automatizados

Execute os testes utilizando:

```bash
pytest
```

---

## Testes com cobertura

```bash
pytest --cov=scraper --cov-report=term-missing
```

---

# 🧹 Limpeza de Cache

## Linux/macOS

```bash
rm -rf scraper/__pycache__ tests/__pycache__
```

---

## Windows (PowerShell)

```powershell
Remove-Item -Recurse -Force scraper\__pycache__, tests\__pycache__
```

---

# 📤 Arquivos Gerados

Após a execução, os dados serão exportados para:

```text
books.json
books.csv
```

---

# 📖 Exemplo de Estrutura do JSON

```json
{
  "title": "It's Only the Himalayas",
  "price": "45.17",
  "availability": "In stock",
  "theme": "Self-discovery and travel",
  "target_audience": "Adventure readers",
  "short_summary": "A journey through the Himalayas..."
}
```

---

# 🛠️ Possíveis Melhorias Futuras

* Persistência completa em PostgreSQL
* Dashboard web
* API REST
* Scraping distribuído
* Retry automático
* Proxy rotation
* Async workers
* Exportação para banco vetorial
* Integração com embeddings

---

# 📄 Licença

Este projeto é destinado para fins educacionais e estudos de automação, scraping e integração com IA.

---

# 👨‍💻 Autor

Desenvolvido por João Pedro Lacerda Sousa.
