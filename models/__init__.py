from dotenv import load_dotenv
import os

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
HF_HOME = os.getenv("HF_HOME")
MODEL_ID = "Kostya165/rubert_tiny2_russian_emotion_sentiment"

os.environ["HF_TOKEN"] = HF_TOKEN
os.environ['HF_HOME'] = HF_HOME