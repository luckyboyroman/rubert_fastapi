FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt
COPY requirements.txt .

# Сначала устанавливаем PyTorch с CUDA поддержкой
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# Затем остальные зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Запускаем FastAPI через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]