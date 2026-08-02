# rubert_fastapi
Проект по разработке FastAPI приложения для проверки инференса модели rubert base cased и rubert-tiny2

Структура проекта
```
rubert_fastapi/
├── main.py                 # Основной файл приложения
├── Dockerfile              # Dockerfile для сборки образа
├── requirements.txt        # Зависимости проекта
├── .env                    # Переменные окружения
├── models/                 # Пакет с моделями
│   ├── __init__.py
│   ├── rubert_model.py    # Класс для работы с ruBERT моделью
│   └── pydantic_models.py # Pydantic модели для валидации данных
└── README.md              # Документация проекта
```


Запуск через Uvicorn
```
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

Cборка и запуск Docker образа

```
docker build -t rubert_api .
docker run -d -p 8080:8080 rubert_api
```

Запуск pytest

```
pytest test_app.py -v
```