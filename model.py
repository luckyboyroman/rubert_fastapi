from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_HOME = os.getenv("HF_HOME")

os.environ["HF_TOKEN"] = HF_TOKEN
os.environ['HF_HOME'] = HF_HOME


# Загружаем модель и токенизатор
MODEL_ID = "Kostya165/rubert_tiny2_russian_emotion_sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model12    = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
model12.eval()

texts = [
    "Сегодня отличный день!",
    "Меня это всё бесит и раздражает."
]

# Токенизация
enc = tokenizer(texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
with torch.no_grad():
    logits = model12(**enc).logits
    preds = logits.argmax(dim=-1).tolist()

# Преобразуем ID обратно в метки
id2label = model12.config.id2label
labels = [id2label[p] for p in preds]
print(labels)  # например: ['positive', 'aggression']