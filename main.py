from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return 'Привет, это будущее приложение по FastAPI с тестирование модели rubert'