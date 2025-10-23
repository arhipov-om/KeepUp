# KeepUp — Open Source SaaS Uptime Monitor

**KeepUp** — это **open Source веб-сервис для мониторинга доступности сайтов**. Автоматически проверяет HTTP-статус доменов по расписанию, сохраняет историю и отображает статус в реальном времени.

Подходит для self-hosted развертывания или использования как SaaS-платформы.

---

## Возможности

- Проверка сайтов каждые 60 секунд (настраивается)
- История проверок и графики доступности
- REST API + Swagger UI
- Поддержка нескольких пользователей
- Асинхронные задачи через Taskiq + Redis
- Clean Architecture + FastAPI
- Полная поддержка Docker

---

## Технологии

| Слой | Технология |
|------|------------|
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.0 |
| БД | PostgreSQL |
| Очереди | Redis + Taskiq |
| Миграции | Alembic |
| Фронтенд | React + TypeScript (в разработке) |
| DevOps | Docker, docker-compose, UV |

---

## Быстрый старт (Docker)

```bash
git clone https://github.com/yourusername/keepup.git
cd keepup

cp backend/.env.example backend/.env
docker-compose up --build
```

Доступно:
- **API**: `http://localhost:8000`
- **Документация**: `http://localhost:8000/docs`
- **Фронтенд**: `http://localhost:3000` *(в разработке)*

---

## Локальная разработка

```bash
# Backend
cd backend
uv sync
cp .env.example .env
alembic upgrade head
uvicorn main:app --reload

# Воркер (в отдельном терминале)
python worker.py
```

---

## API

Документация: **Swagger** — `/docs`, **ReDoc** — `/redoc`

---

## Задачи

- `check_domain_task` — проверка одного сайта
- Запускается по расписанию через встроенный планировщик

---

## Тестирование

```bash
pytest
```

---

## Контрибьютинг

1. Форк → ветка → коммит → PR
2. Следуйте [Code of Conduct](CODE_OF_CONDUCT.md)
3. Используйте [pre-commit](https://pre-commit.com/) (в планах)

---

## Лицензия

[MIT License](LICENSE) — свободное использование, модификация и коммерческое применение.

---

**KeepUp — ваш надежный uptime-монитор. Self-host или SaaS — на ваш выбор.**