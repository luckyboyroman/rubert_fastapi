from fastapi import FastAPI
from models.rubert_model import RubertModel

texts = [
    "Сегодня отличный день!",
    "Меня это всё бесит и раздражает."
]
model = RubertModel()
model.classify_text(texts)

# app = FastAPI()

# @app.get('/')
# def home():
#     return 'Привет, это будущее приложение по FastAPI с тестирование модели rubert'