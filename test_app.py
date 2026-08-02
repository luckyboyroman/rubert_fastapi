import pytest
from fastapi.testclient import TestClient
from main import app

# Создаем тестовый клиент
client = TestClient(app)

def test_home_endpoint():
    """Тест главной страницы"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "model_name" in data
    assert "max_length" in data
    assert "classes" in data
    assert "device" in data
    assert "Привет" in data["message"]

def test_model_info_endpoint():
    """Тест эндпоинта с информацией о модели"""
    response = client.get("/model-info")
    
    assert response.status_code == 200
    data = response.json()
    assert "model_name" in data
    assert "max_length" in data
    assert "classes" in data
    assert "id2label" in data
    assert "label2id" in data
    assert "device" in data

def test_classify_single_text():
    """Тест классификации одного текста"""
    test_data = {
        "texts": ["Это отличный фильм!"]
    }
    
    response = client.post("/classify", json=test_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total" in data
    assert data["total"] == 1
    assert len(data["results"]) == 1
    assert "input_text" in data["results"][0]
    assert "label" in data["results"][0]

def test_classify_multiple_texts():
    """Тест классификации нескольких текстов"""
    test_data = {
        "texts": [
            "Это отличный фильм!",
            "Ужасный сервис, не рекомендую.",
            "Нейтральный отзыв."
        ]
    }
    
    response = client.post("/classify", json=test_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["results"]) == 3
    
    # Проверяем, что каждый результат содержит текст и метку
    for result in data["results"]:
        assert "input_text" in result
        assert "label" in result

def test_classify_with_empty_list():
    """Тест с пустым списком текстов"""
    test_data = {
        "texts": []
    }
    
    response = client.post("/classify", json=test_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["results"]) == 0

def test_classify_validation_error():
    """Тест валидации - неверные данные"""
    test_data = {
        "not_texts": ["ошибка"]  # Неправильное поле
    }
    
    response = client.post("/classify", json=test_data)
    assert response.status_code == 422  # Validation error