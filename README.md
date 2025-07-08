# Projeto: API FastAPI com Automações via Celery + Redis

Este projeto demonstra como estruturar uma aplicação web escalável em Python com **FastAPI** para expor endpoints e **Celery** com **Redis** para executar automações assíncronas, desacoplando o processamento da API.

---

## 📁 Estrutura de Pastas

```bash
projeto_rpa/
├── app/
│   ├── api/                  # Endpoints da API
│   ├── core/                 # Configurações (Celery, Settings)
│   ├── services/             # Lógica de automação
│   ├── workers/              # Worker Celery
│   ├── main.py               # FastAPI app
│   └── __init__.py
├── run_worker.py            # Entrypoint do Celery
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
```

---

## 🚀 Tecnologias Usadas

- Python 3.10
- FastAPI
- Celery 5.5
- Redis 7
- Uvicorn
- Docker e Docker Compose

---

## 🧰 Pré-requisitos

- Docker
- Docker Compose

---

## ▶️ Como Executar Localmente

```bash
# 1. Clonar o repositório
$ git clone https://github.com/seu-usuario/projeto-rpa-fastapi-celery.git
$ cd projeto-rpa-fastapi-celery

# 2. Subir a stack
$ docker-compose up --build
```

A aplicação ficará disponível em `http://localhost:8000` e a documentação em `http://localhost:8000/docs`

---

## 🧪 Testando o Endpoint

```bash
curl -X POST http://localhost:8000/executar \
     -H "Content-Type: application/json" \
     -d '{"cliente_id": 123}'
```

Você verá os logs da automação sendo executada no container `worker`.

---

## 📦 Comandos Úteis

```bash
# Reiniciar stack
$ docker-compose down --volumes && docker-compose build && docker-compose up

# Acessar container
$ docker exec -it nome-do-container bash
```

---




> Feito por Matheus Lima 
