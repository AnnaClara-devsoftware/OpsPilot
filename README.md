# OpsPilot

> Plataforma web para análise estática, auditoria de código e métricas de projetos de software.

[![Python Version](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

O **OpsPilot** é uma plataforma distribuída projetada para automatizar o processo de análise estática em arquivos de código fonte (`.zip`). A aplicação processa métricas de linhas de código (LOC), dependências, arquivos de grande porte, pendências (`TODO`/`FIXME`), complexidade ciclomática e varredura heurística de vazamento de segredos/credenciais. 

Todo o processamento de arquivos é executado de forma **assíncrona via workers dedicados**, garantindo alta disponibilidade e separação de responsabilidades na infraestrutura.

---

## Sumário

- [Visão Geral e Fluxo de Dados](#-visão-geral-e-fluxo-de-dados)
- [Arquitetura de Sistemas](#-arquitetura-de-sistemas)
- [Stack Tecnológica](#-stack-tecnológica)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Principais Funcionalidades](#-principais-funcionalidades)
- [Execução Local (Docker & Compose)](#-execução-local-docker--compose)
- [Execução para Desenvolvimento (Sem Docker)](#-execução-para-desenvolvimento-sem-docker)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Suíte de Testes](#-suíte-de-testes)
- [Implantação e Infraestrutura (Deploy)](#-implantação-e-infraestrutura-deploy)
- [Práticas de Segurança](#-práticas-de-segurança)
- [Autora](#-autora)

---

## Visão Geral e Fluxo de Dados

[ Usuário ] ──► (Upload .zip) ──► [ FastAPI ] ──► (Cria Job: 'pending')
│
▼
[ Redis Message Broker ]
│
▼
[ Celery Worker Pool ]
│
(Descompactação segura / Sanitização / Análise)
│
▼
[ Banco Postgres (Neon) ]
│
▼
[ Dashboard React ] ◄── (Query Analytics & Reports) ───┘

---

## Arquitetura de Sistemas

A aplicação adota uma arquitetura em camadas desacoplada e escalável:

┌──────────────────────────┐         REST / HTTPS         ┌──────────────────────────┐
│     Frontend Web         │ ───────────────────────────► │      Backend API         │
│  React 18 + TS + Vite    │ ◄─────────────────────────── │  FastAPI (Python 3.13)   │
│   Tailwind CSS (Vercel)  │                              │  Auth JWT + Rate Limit   │
└──────────────────────────┘                              └────────────┬─────────────┘
│
┌──────────────────────────────┼──────────────────────────────┐
▼                              ▼                              ▼
┌─────────────────────┐        ┌─────────────────────┐        ┌─────────────────────┐
│  PostgreSQL (Neon)  │        ┌  Redis (Upstash)    │        │   Workers Celery    │
│  Camada de Dados    │        │  Broker de Mensagens│        │ Processamento Async │
└─────────────────────┘        └─────────────────────┘        └─────────────────────┘


### Padrão de Camadas Interno (Backend)
`API (Routes)` ➔ `Services (Regras de Negócio & Scanner)` ➔ `Repositories (Acesso a Dados)` ➔ `Models (SQLAlchemy)`
*Validação de dados com Schemas Pydantic em todas as fronteiras da aplicação.*

---

## Stack Tecnológica

| Camada | Tecnologias / Ferramentas |
| :--- | :--- |
| **Backend** | Python 3.13, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, Pytest |
| **Processamento Assíncrono** | Celery, Redis |
| **Banco de Dados** | PostgreSQL (Driver `psycopg3`), SQLite (Testes) |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, React Router, Recharts |
| **DevOps & Infra** | Docker, Docker Compose, Render (API + Workers), Neon DB, Upstash, Vercel |

---

## Estrutura do Repositório

```text
opspilot/
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── services/
│   │   ├── workers/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── utils/
│   │   └── core/
│   ├── alembic/
│   ├── tests/
│   ├── Dockerfile
│   └── Dockerfile.worker
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── context/
│   │   ├── services/
│   │   └── types/
│   └── Dockerfile
├── docker-compose.yml
├── render.yaml
└── README.md
```

## Principais Funcionalidades

**Autenticação & Segurança:** Fluxo JWT de curta duração com sistema de Refresh Tokens, criptografia de senhas via bcrypt e suporte a Rate Limiting.
**Upload Sanitizado:** Proteção nativa contra vulnerabilidades de descompactação (Zip-Slip e Zip-Bomb), validação de MIME types e limite configurável de payload.
**Mecanismo de Análise Estática:** 
● Contagem de linhas de código (LOC) por linguagem.
● Varredura e mapeamento de dependências (requirements.txt, package.json, etc.).
● Detecção heurística de credenciais e segredos expostos (tokens AWS, chaves API, senhas hardcoded).
● Análise de dívida técnica (TODO / FIXME) e aproximação de complexidade ciclomática.
● Pipeline de Workers Assíncronos: Gestão de estado de filas (pending ➔ processing ➔ completed / failed) com lógica de retry automático e backoff exponencial.
● Exportação de Relatórios: Geração e download de relatórios consolidados nos formatos HTML, JSON e CSV.

## Execução Local (Docker & Compose)

**Pré-requisitos**
- Docker Desktop (Engine 20.10+)
- Docker Compose

**Instalação e inicialização**

Clone este repositório:
```bash
git clone https://github.com/Annaa-Clara/opspilot.git
cd opspilot
```

Defina os arquivos de ambiente:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Suba o ecossistema completo:
```bash
docker compose up --build
```

**Aplicações disponíveis após a inicialização:**

| Serviço | URL |
| :--- | :--- |
| Frontend App | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| OpenAPI / Swagger Docs | http://localhost:8000/api/docs |

---

## Execução para Desenvolvimento (Sem Docker)

**Backend (API & Worker)**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements-dev.txt
cp .env.example .env

alembic upgrade head

uvicorn app.main:app --reload
```

Em um terminal separado (mesmo venv ativo):
```bash
celery -A app.core.celery_app.celery_app worker --loglevel=info
```

**Frontend**
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## Variáveis de Ambiente

**Backend (`backend/.env`)**

| Variável | Descrição | Valor Exemplo / Padrão |
| :--- | :--- | :--- |
| `SECRET_KEY` | Chave secreta para assinatura dos tokens JWT | `string_segura_comprida` |
| `ALGORITHM` | Algoritmo criptográfico dos tokens | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do Token de Acesso | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Tempo de expiração do Refresh Token | `7` |
| `DATABASE_URL` | String de Conexão Postgres (Driver psycopg) | `postgresql+psycopg://user:pass@host:5432/db` |
| `REDIS_URL` | URL de Conexão com a Fila Redis | `redis://host:6379/0` |
| `ALLOWED_ORIGINS` | Origens autorizadas para requisições CORS | `https://sua-app.vercel.app` |
| `MAX_UPLOAD_SIZE_MB` | Limite máximo do arquivo ZIP enviado | `50` |

**Frontend (`frontend/.env`)**

| Variável | Descrição | Valor Exemplo / Padrão |
| :--- | :--- | :--- |
| `VITE_API_BASE_URL` | Endpoint base de comunicação com a API | `https://api.opspilot.com/api/v1` |

---

## Suíte de Testes

Os testes automatizados utilizam SQLite em memória para a camada de backend, dispensando dependências externas (Postgres/Redis) no ambiente de testes.

**Executar testes de Backend**
```bash
cd backend
source .venv/bin/activate
pytest -v
```

**Executar testes de Frontend**
```bash
cd frontend
npm run test
```

---

## Implantação e Infraestrutura (Deploy)

A arquitetura do projeto foi desenhada para fácil implantação em serviços de nuvem modernos:

- **Database:** Serverless PostgreSQL via Neon DB.
- **Cache & Message Broker:** Serverless Redis via Upstash.
- **Backend API & Workers:** Hospedagem containerizada via Render, utilizando a especificação do `render.yaml`.
- **Frontend Web:** Deploy contínuo via Vercel.

---

## Práticas de Segurança

- Hash de senhas armazenado via algoritmos fortes com salting (bcrypt).
- Isolamento de processamento de arquivos compactados e prevenção de exaustão de recursos.
- Validação estrita de parâmetros de entrada utilizando Pydantic em todas as rotas da API REST.
- Middleware configurado para restrição de requisições maliciosas por IP (Rate Limiting).

---

## Autora

Desenvolvido por **Anna Clara de Medeiros Gonçalves**.

- **LinkedIn:** [Anna Clara de Medeiros Gonçalves](https://www.linkedin.com/in/anna-clara-de-medeiros-gon%C3%A7alves-b6537a2ba)
- **GitHub:** [@Annaa-Clara](https://github.com/Annaa-Clara)
- **Portfólio:** [Acesse meu Portfólio](https://annaa-clara.github.io/anna-clara-portfolio/)
