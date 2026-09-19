# 🚀 OpsPilot

**Plataforma web para automação e análise de projetos de software.**

O usuário envia um projeto (arquivo `.zip`) e o OpsPilot analisa automaticamente estrutura, linguagens, linhas de código, dependências, arquivos grandes, TODOs/FIXMEs, possíveis segredos expostos e complexidade — tudo processado de forma assíncrona por workers, com dashboard, histórico e relatórios exportáveis (HTML, JSON, CSV).

Projeto construído para demonstrar competências de portfólio em: **Python, arquitetura de sistemas, automação, filas/workers, análise estática de código, backend, banco de dados e deploy em produção.**

---

## Índice

1. [Visão geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Stack tecnológica](#stack-tecnológica)
4. [Estrutura de pastas](#estrutura-de-pastas)
5. [Funcionalidades](#funcionalidades)
6. [Rodando localmente](#rodando-localmente)
7. [Variáveis de ambiente](#variáveis-de-ambiente)
8. [Testes](#testes)
9. [Deploy em produção](#deploy-em-produção)
10. [Segurança](#segurança)
11. [Guia passo a passo para iniciantes](#guia-passo-a-passo-para-iniciantes)

---

## Visão geral

```
Usuário → Upload .zip → API valida e salva → Job criado (pending)
                                                   │
                                                   ▼
                                  Worker Celery pega o job (processing)
                                                   │
                          extrai zip → varre arquivos → calcula métricas
                          → detecta TODOs/segredos → gera relatórios
                                                   │
                                                   ▼
                                  Job = completed (ou failed com retry)
                                                   │
                                                   ▼
                     Dashboard exibe estatísticas, histórico e relatórios
```

## Arquitetura

```
┌─────────────────┐        HTTPS/REST        ┌──────────────────────┐
│   Frontend       │ ────────────────────────▶│   Backend (FastAPI)   │
│ React+TS+Vite     │◀──────────────────────── │  API + Auth JWT       │
│ Tailwind (Vercel) │                          │  (Render)             │
└─────────────────┘                          └──────────┬────────────┘
                                                          │
                                    ┌─────────────────────┼─────────────────────┐
                                    ▼                     ▼                     ▼
                          ┌─────────────────┐   ┌──────────────────┐  ┌──────────────────┐
                          │  PostgreSQL      │   │  Redis (fila)     │  │  Workers Celery   │
                          │  (Neon)          │   │  (Upstash)        │  │  (Render worker)  │
                          └─────────────────┘   └──────────────────┘  └──────────────────┘
```

**Fluxo de camadas do backend:** `api/` (rotas HTTP) → `services/` (regras de negócio e análise) → `repositories/` (acesso a dados) → `models/` (SQLAlchemy) — com `schemas/` (Pydantic) validando entrada/saída, `workers/` executando os jobs assíncronos e `core/` concentrando configuração, segurança e infraestrutura compartilhada.

## Stack tecnológica

| Camada     | Tecnologias |
|------------|-------------|
| Backend    | Python 3.13, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, Pytest |
| Fila/Workers | Celery, Redis |
| Banco de dados | PostgreSQL (Neon em produção) |
| Frontend   | React 18, TypeScript, Vite, Tailwind CSS, React Router, Recharts |
| Infra      | Docker, Docker Compose |
| Deploy     | Render (API + worker), Neon (Postgres), Upstash (Redis), Vercel (frontend) |

## Estrutura de pastas

```
opspilot/
├── backend/
│   ├── app/
│   │   ├── api/routes/        # Endpoints HTTP (auth, projects, uploads, analyses, jobs, reports, dashboard)
│   │   ├── services/          # Motor de análise: scanner, linguagens, TODOs, segredos, complexidade, relatórios
│   │   ├── workers/           # Tasks Celery (pipeline de análise assíncrona)
│   │   ├── models/            # Modelos SQLAlchemy (users, projects, analyses, jobs, reports, metrics)
│   │   ├── repositories/      # Camada de acesso a dados
│   │   ├── schemas/           # Schemas Pydantic (validação/serialização)
│   │   ├── utils/             # Utilitários (extração segura de ZIP)
│   │   └── core/              # Config, segurança/JWT, database, celery app, rate limit
│   ├── alembic/                # Migrations
│   ├── tests/                  # Testes Pytest (22 testes)
│   ├── Dockerfile               # Imagem da API
│   └── Dockerfile.worker        # Imagem do worker Celery
├── frontend/
│   ├── src/
│   │   ├── pages/               # Landing, Login, Register, Dashboard, AnalysisDetail, Jobs, Reports, Settings
│   │   ├── components/          # Sidebar, StatCard, StatusBadge, ProtectedRoute
│   │   ├── context/              # AuthContext (JWT + refresh token)
│   │   ├── services/              # Cliente Axios + serviços de API
│   │   └── types/                  # Tipos TypeScript compartilhados
│   └── Dockerfile
├── docker-compose.yml
├── render.yaml
└── README.md
```

## Funcionalidades

- **Autenticação:** registro, login, JWT de acesso + refresh token, renovação automática no frontend.
- **Upload seguro:** ZIP com limite de tamanho, validação de extensão e proteção contra zip-slip/zip-bomb.
- **Análise automática:** estrutura, linguagens, LOC, dependências (`requirements.txt`, `package.json`, etc.), arquivos grandes, TODO/FIXME, heurística de segredos expostos (chaves AWS, tokens, senhas em texto plano, etc.) e complexidade ciclomática aproximada.
- **Workers assíncronos:** pipeline completo rodando em Celery, com progresso, logs, tempo de execução, contagem de tentativas e retry automático com backoff em caso de falha.
- **Fila com estados:** `pending → processing → completed | failed`, com `retry` intermediário.
- **Relatórios:** exportação em HTML (visual), JSON (estruturado) e CSV (planilha).
- **Dashboard:** estatísticas agregadas, gráfico de status dos jobs, histórico de análises e projetos.
- **Segurança:** rate limiting por IP, CORS configurável, senhas com bcrypt, JWT assinado, upload sanitizado.

## Rodando localmente

### Pré-requisitos
- Docker e Docker Compose instalados.

### Passos

```bash
# 1. Clone o repositório
git clone <url-do-seu-repositorio>
cd opspilot

# 2. Configure as variáveis de ambiente do backend
cp backend/.env.example backend/.env
# edite backend/.env se quiser mudar algo (os valores padrão já funcionam com o compose)

# 3. Configure o frontend
cp frontend/.env.example frontend/.env

# 4. Suba tudo
docker compose up --build
```

Isso sobe: PostgreSQL, Redis, a API (`http://localhost:8000`), o worker Celery e o frontend (`http://localhost:5173`).

A documentação interativa da API fica em `http://localhost:8000/api/docs`.

### Rodando sem Docker (desenvolvimento)

**Backend:**
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env   # ajuste DATABASE_URL/REDIS_URL para instâncias locais
alembic upgrade head
uvicorn app.main:app --reload
```

**Worker (em outro terminal, mesmo venv):**
```bash
celery -A app.core.celery_app.celery_app worker --loglevel=info
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Variáveis de ambiente

### Backend (`backend/.env`)

| Variável | Descrição | Exemplo |
|---|---|---|
| `SECRET_KEY` | Chave usada para assinar os JWTs | string aleatória longa |
| `ALGORITHM` | Algoritmo do JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Validade do access token | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Validade do refresh token | `7` |
| `DATABASE_URL` | Conexão PostgreSQL (SQLAlchemy) | `postgresql+psycopg://user:pass@host:5432/db` |
| `REDIS_URL` | Conexão Redis (fila do Celery) | `redis://host:6379/0` |
| `ALLOWED_ORIGINS` | Origens permitidas no CORS | `https://seuapp.vercel.app` |
| `MAX_UPLOAD_SIZE_MB` | Limite de upload de ZIP | `50` |
| `UPLOAD_DIR` | Diretório temporário de uploads | `/tmp/opspilot_uploads` |
| `RATE_LIMIT` | Limite de requisições por IP | `100/minute` |

### Frontend (`frontend/.env`)

| Variável | Descrição | Exemplo |
|---|---|---|
| `VITE_API_BASE_URL` | URL base da API | `https://opspilot-api.onrender.com/api/v1` |

## Testes

**Backend (22 testes, usando SQLite em memória — não precisa de Postgres/Redis rodando):**
```bash
cd backend
source .venv/bin/activate
pytest -v
```

**Frontend:**
```bash
cd frontend
npm run test
```

## Deploy em produção

Veja o [guia passo a passo para iniciantes](#guia-passo-a-passo-para-iniciantes) abaixo — ele cobre Neon, Upstash, Render, Vercel e GitHub do zero.

Resumo técnico:
- **Neon:** crie um banco Postgres e copie a *connection string* para `DATABASE_URL`.
- **Upstash:** crie um banco Redis e copie a URL para `REDIS_URL`.
- **Render:** use o `render.yaml` (Blueprint) na raiz do repositório para subir a API e o worker de uma vez, ou crie os dois serviços manualmente com os `Dockerfile`/`Dockerfile.worker`.
- **Vercel:** aponte para a pasta `frontend`, com `VITE_API_BASE_URL` configurado para a URL pública da API no Render.

## Segurança

- Senhas com hash `bcrypt` (nunca armazenadas em texto plano).
- JWT de acesso de curta duração + refresh token de longa duração.
- Rate limiting por IP em rotas sensíveis (`slowapi`).
- CORS restrito às origens configuradas.
- Upload de ZIP validado por extensão, tamanho máximo e proteção contra path traversal (zip-slip) e zip bomb.
- Scanner heurístico de segredos (chaves de API, tokens, senhas em texto plano, URLs de banco com credenciais) rodando em toda análise.

---

## Guia passo a passo para iniciantes

Este guia assume que você nunca fez deploy de nada. Vamos com calma.

### 1. Como abrir o projeto

Descompacte o arquivo `.zip` que você recebeu em uma pasta no seu computador (ex: `Documentos/opspilot`). Abra essa pasta no VS Code (ou seu editor preferido).

### 2. Como instalar as dependências

Você precisa ter instalado: [Python 3.13](https://www.python.org/downloads/), [Node.js 22+](https://nodejs.org/) e [Docker Desktop](https://www.docker.com/products/docker-desktop/) (mais fácil) — ou Python/Node locais se preferir não usar Docker.

**Caminho mais simples (Docker):** basta ter o Docker Desktop instalado e aberto.

### 3. Como configurar o `.env`

Dentro da pasta `backend`, copie o arquivo de exemplo:
```bash
cp backend/.env.example backend/.env
```
Abra `backend/.env` num editor de texto. Para rodar localmente, os valores padrão já funcionam. Troque apenas `SECRET_KEY` por uma string aleatória longa (pode gerar uma em https://randomkeygen.com/).

Faça o mesmo para o frontend:
```bash
cp frontend/.env.example frontend/.env
```

### 4. Como subir localmente

Na raiz do projeto (pasta `opspilot`), rode:
```bash
docker compose up --build
```
Aguarde as mensagens de log pararem de "pular" muito — quando aparecer `Uvicorn running on http://0.0.0.0:8000` a API está de pé. Abra `http://localhost:5173` no navegador para ver o site, e `http://localhost:8000/api/docs` para ver a documentação da API.

### 5. Como criar um banco no Neon

1. Acesse https://neon.tech e crie uma conta gratuita.
2. Clique em "Create a project", dê um nome (ex: `opspilot`) e escolha uma região.
3. Na página do projeto, copie a **Connection String** (algo como `postgresql://usuario:senha@ep-xxxx.neon.tech/neondb?sslmode=require`).
4. Troque o prefixo `postgresql://` por `postgresql+psycopg://` e cole no `DATABASE_URL` (no Render, você vai colar isso como variável de ambiente — veja o passo 7).

### 6. Como criar um Redis no Upstash

1. Acesse https://upstash.com e crie uma conta gratuita.
2. Clique em "Create Database", escolha o tipo Redis, dê um nome e escolha uma região próxima do seu backend (Render costuma usar Oregon/US).
3. Na página do banco, copie a URL no formato `rediss://...` (Upstash já fornece pronta para uso).
4. Essa URL vai virar a variável `REDIS_URL` no Render.

### 7. Como fazer deploy no Render

1. Acesse https://render.com e crie uma conta (dá para logar com GitHub).
2. Clique em "New +" → "Blueprint" e selecione o repositório do OpsPilot no GitHub (veja o passo 9 se ainda não subiu pro GitHub).
3. O Render vai detectar o arquivo `render.yaml` na raiz e propor criar dois serviços: `opspilot-api` (web) e `opspilot-worker` (worker).
4. Antes de confirmar, preencha as variáveis marcadas como "sync: false":
   - `DATABASE_URL` → a connection string do Neon (com `postgresql+psycopg://`).
   - `REDIS_URL` → a URL do Upstash.
   - `ALLOWED_ORIGINS` → a URL do seu frontend na Vercel (ex: `https://opspilot.vercel.app`), depois de feito o passo 8.
5. Clique em "Apply" e aguarde o build. Quando terminar, copie a URL pública da API (ex: `https://opspilot-api.onrender.com`).

### 8. Como fazer deploy na Vercel

1. Acesse https://vercel.com e crie uma conta (pode logar com GitHub).
2. Clique em "Add New..." → "Project" e selecione o repositório do OpsPilot.
3. Em "Root Directory", selecione a pasta `frontend`.
4. Em "Environment Variables", adicione `VITE_API_BASE_URL` com o valor `https://opspilot-api.onrender.com/api/v1` (troque pela URL real da sua API no Render, com `/api/v1` no final).
5. Clique em "Deploy". Ao terminar, a Vercel te dá uma URL pública (ex: `https://opspilot.vercel.app`).
6. Volte no Render e atualize a variável `ALLOWED_ORIGINS` da API com essa URL da Vercel, para o CORS liberar o acesso.

### 9. Como colocar no GitHub

1. Crie uma conta em https://github.com se ainda não tiver.
2. No site do GitHub, clique em "New repository", dê um nome (ex: `opspilot`) e crie (pode deixar privado ou público).
3. No terminal, dentro da pasta do projeto:
```bash
git init
git add .
git commit -m "Primeiro commit do OpsPilot"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/opspilot.git
git push -u origin main
```
4. Pronto — agora o Render e a Vercel conseguem enxergar o repositório para fazer deploy automático a cada `git push`.

---

**Bom projeto de portfólio! 🎯** Qualquer dúvida durante o deploy, revise as variáveis de ambiente primeiro — a maioria dos problemas de "não conecta" vem de uma `DATABASE_URL`, `REDIS_URL` ou `ALLOWED_ORIGINS` mal configurada.
