from fastapi import FastAPI, HTTPException, Body
from sentence_transformers import SentenceTransformer, util
from models.rubert_model import RubertModel
from models.pydantic_models import InputTexts

app = FastAPI()
rubert_model = RubertModel()

@app.get('/')
async def home():
    return 'Привет, это будущее приложение по FastAPI с тестирование моделей семейства rubert'

@app.post("/classify")
async def classify_texts(request: InputTexts):
    labels = rubert_model.classify_text(texts=request.texts)

    results = [
        {"input_text": text, "label": label}
        for text, label in zip(request.texts, labels)
    ]
    return {"results": results, "total": len(results)}

@app.get("/model-info")
async def get_model_info():
    """Информация о загруженной модели"""
    return {
        "model_name": rubert_model.model_id,
        "max_length": rubert_model.max_length,
        "classes": rubert_model.classes,
        "device": str(rubert_model.device)
    }