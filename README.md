# DeNet-Python-Hero

# Тестовое задание

## Требования

- Python 3.8+
- PostgreSQL (для production) или SQLite (для разработки)
- Виртуальное окружение Python (рекомендуется)

## Установка

1. Клонируйте репозиторий и переключитесь на нужную ветку:

```bash
git clone
cd backend/main
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории проекта:
```
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=postgresql://user:pass@localhost/erp_db  # для production
```
>  Если используется SQLite, файл dev.db будет создан автоматически при первом запуске.

## Запуск

### Режим разработки

```bash
python init_db.py
python run_dev.py
```

> Приложение будет доступно по адресу: http://127.0.0.1:7020 
>
> Swagger-UI доступна по адресу: http://127.0.0.1:7020/api/docs
