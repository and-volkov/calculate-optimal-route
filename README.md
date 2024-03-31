# FastAPI Calculate optimal route

Fastapi сервис для расчета оптимального маршрута

### Функционал

- Получить файл csv с данными о маршруте, расчитать оптимальный маршрут и вернуть его в виде json, а также сохранить в базу данных
- Вернуть маршрут по id

### Недостающие эндпонты (Вопрос из задания)

- Получить список всех маршрутов
- Удалить маршрут по id
- Обновить маршрут по id

### Стек технологий

- FastAPI
- PostgreSQL
- Docker
- Docker Compose
- Pydantic
- SQLAlchemy
- Alembic

### Предварительные требования

- Docker
- Docker Compose
- Make (опционально)

### Установка

1. Клонировать репозиторий

```bash
git clone https://github.com/and-volkov/calculate-optimal-route
```

2. Перейти в директорию проекта

```bash
cd calculate-optimal-route
```

3. Скопировать файл `example.env` в `.env`

```bash
cp example.env .env
```

4. Build and run the Docker containers

```bash
docker-compose up --build
```

Или с помощью Make

```bash
make compose
```

5. Применить миграции

```bash
docker compose exec app alembic upgrade head
```

6. Запустить тесты

```bash
pytest
```

### Документация

Документация доступна по адресу http://127.0.0.1/api/v1/docs или http://127.0.0.1/api/v1/redoc

### PGAdmin

PGAdmin доступен по адресу http://127.0.0.1:8888/login

- Email:

```
example@example.com
```

- Password:

```
example
```
