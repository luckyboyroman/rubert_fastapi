from dotenv import load_dotenv
import os

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_HOME = os.getenv("HF_HOME")
MODEL_ID = "Kostya165/rubert_tiny2_russian_emotion_sentiment"

os.environ["HF_TOKEN"] = HF_TOKEN
os.environ['HF_HOME'] = HF_HOME



# # Загружаем дообученную модель для сходства текстов
# # (вместо базовой, т.к. она сразу дает качественные эмбеддинги)
# model = SentenceTransformer("DeepPavlov/rubert-base-cased") 

# # Примеры предложений
# sentences = [
#     'Сегодня на улице хорошая погода',
#     'Отличная погодка сегодня выдалась',
#     'Мне нужно купить продукты в магазине'
# ]

# # Получаем эмбеддинги
# embeddings = model.encode(sentences)

# # Вычисляем матрицу сходства (косинусное расстояние)
# cosine_scores = util.cos_sim(embeddings, embeddings)

# # Смотрим на близость первого предложения к остальным
# print(cosine_scores[0])