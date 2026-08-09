from fastapi import FastAPI, HTTPException, Body, Request, Response
from sentence_transformers import SentenceTransformer, util
from models.rubert_model import RubertModel
from models.pydantic_models import InputTexts
from models.database import setup_database, SessionDep, RequestLog, new_session
from contextlib import asynccontextmanager
import logging
import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Lifespan для инициализации БД при старте
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Инициализация базы данных логов...")
    await setup_database()
    yield
    logger.info("Завершение работы приложения")

app = FastAPI(lifespan=lifespan)                 # FastAPI приложение
rubert_model = RubertModel()    # Модель ruBERT для классификации текстов


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Логирование всех HTTP запросов через middleware"""
    start_time = time.time()
    
    method = request.method
    path = request.url.path
    headers = dict(request.headers)
    
    logger.info(f"Метод: {method} {path}")
    logger.info(f"Заголовки: {headers}")
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        
        # Вычисляем время выполнения
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time) # Добавление пользовательского заголовка, для отслеживания времени работы
        
        # Логируем ответ
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Process time: {process_time:.4f} seconds")
        
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise

    finally:
        try:
            async with new_session() as session:
                log_entry = RequestLog(
                    method=method,
                    path=path,
                    headers=headers,
                    status_code=status_code,
                    process_time=round(process_time, 4),
                )
                session.add(log_entry)
                await session.commit()
                logger.info("Закомитили")
        except Exception as db_err:
            # КРИТИЧНО: Ошибка логирования не должна возвращать 500 пользователю
            logger.error(f"Failed to save log to DB: {db_err}", exc_info=True)


@app.get("/", summary="Главная страница", description="Главная страница, содержит информацию о загруженной модели")
async def home():
    """Начальная страница, возращает основную информацию о загруженной модели ruBERT"""

    return {
        "message": "Привет, это приложение на FastAPI для проверки и тестирования работы моделей семейства ruBERT",
        "model_name": rubert_model.model_id,
        "max_length": rubert_model.max_length,
        "classes": rubert_model.classes,
        "device": str(rubert_model.device)
    }

@app.post("/classify", summary="Классификация текстов", description="Принимает список текстов на русском языке и возвращает для каждого предсказанный класс")
async def classify_texts(request: InputTexts):
    """Функция для классификации текстов"""

    labels = rubert_model.classify_text(texts=request.texts)

    results = [
        {"input_text": text, "label": label}
        for text, label in zip(request.texts, labels)
    ]
    return {"results": results, "total": len(results)}

@app.get("/model-info", summary="Информация о модели", description="Возвращает детальную информацию о загруженной модели: название, максимальную длину, соответствие ID и меток")
async def get_model_info():
    """ Получение более подробной информации о модели"""

    return {
        "model_name": rubert_model.model_id,
        "max_length": rubert_model.max_length,
        "classes": rubert_model.classes,
        "id2label": rubert_model.id2label,
        "label2id": rubert_model.label2id,
        "device": str(rubert_model.device)
    }

