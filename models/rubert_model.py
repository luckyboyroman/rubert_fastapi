from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer, util
import torch
import os
from models import MODEL_ID

class RubertModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        self.model    = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
        self.model_id = MODEL_ID

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.max_length = 128
        self.is_loaded = True
        
        self.id2label = self.model.config.id2label
        self.label2id = self.model.config.label2id
        self.classes = list(self.id2label.values()) if self.id2label else []

    def classify_text(self, texts:list):
        if not texts:
            return []          
        self.model.eval()
        enc = self.tokenizer(
            texts, 
            padding=True, 
            truncation=True, 
            max_length=self.max_length,
            return_tensors="pt"
        )
    
        enc = {k: v.to(self.device) for k, v in enc.items()}
        
        with torch.no_grad():
            logits = self.model(**enc).logits
            preds = logits.argmax(dim=-1)
            
        preds_cpu = preds.cpu().tolist()
        
        # Преобразуем ID обратно в метки
        labels = [self.id2label[p] for p in preds_cpu]
        
        return labels
