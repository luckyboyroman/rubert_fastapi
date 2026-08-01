from fastapi import FastAPI, HTTPException, Body, Request, Response
from sentence_transformers import SentenceTransformer, util
from models.rubert_model import RubertModel
from models.pydantic_models import InputTexts
import logging
import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()
rubert_model = RubertModel()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware для логирования всех входящих запросов"""
    start_time = time.time()
    
    method = request.method
    path = request.url.path
    headers = dict(request.headers)
    
    logger.info(f"➡️  {method} {path}")
    logger.info(f"📋 Заголовки: {headers}")
    
    try:
        response = await call_next(request)
        
        # Вычисляем время выполнения
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        # Логируем ответ
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Process time: {process_time:.4f} seconds")
        
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise

@app.get("/")
async def home():
    return {
        "message": "Привет, это API для классификации текстов с помощью ruBERT",
        "model_name": rubert_model.model_id,
        "max_length": rubert_model.max_length,
        "classes": rubert_model.classes,
        "device": str(rubert_model.device)
    }

@app.post(
    "/classify",
    summary="Классификация текстов",
    description="Принимает список текстов на русском языке и возвращает для каждого предсказанный класс"
)
async def classify_texts(request: InputTexts):
    labels = rubert_model.classify_text(texts=request.texts)

    results = [
        {"input_text": text, "label": label}
        for text, label in zip(request.texts, labels)
    ]
    return {"results": results, "total": len(results)}

@app.get(
    "/model-info",
    summary="Информация о модели",
    description="Возвращает детальную информацию о загруженной модели: название, максимальную длину, соответствие ID и меток"
)
async def get_model_info():
    """
    Получение подробной информации о модели.
    
    Returns:
        dict: Детальная информация о модели ruBERT
    """
    return {
        "model_name": rubert_model.model_id,
        "max_length": rubert_model.max_length,
        "classes": rubert_model.classes,
        "id2label": rubert_model.id2label,
        "label2id": rubert_model.label2id,
        "device": str(rubert_model.device)
    }