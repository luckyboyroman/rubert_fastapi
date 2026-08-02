FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Сначала устанавливаем PyTorch с CUDA поддержкой, т.к. в если поместить в requirements.txt то будет ошибка с адресом скачивания
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запускаем FastAPI через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]