from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
from models import MODEL_ID

class RubertModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        self.model    = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)

    def classify_text(self, texts:list):
        self.model.eval()
        # Токенизация
        enc = self.tokenizer(texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**enc).logits
            preds = logits.argmax(dim=-1).tolist()

        # Преобразуем ID обратно в метки
        id2label = self.model.config.id2label
        labels = [id2label[p] for p in preds]
        print(labels)  # например: ['positive', 'aggression']

