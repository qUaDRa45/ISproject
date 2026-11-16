# Применение ИИ-ассистентов и анализ рисков

## 1. Генерация тестовых сценариев с помощью ИИ
* **Инструмент:** LLM-ассистент (Gemini / GitHub Copilot).
* **Промпт:** *«Напиши модульные тесты на pytest для FastAPI-эндпоинта POST /bookings/, используя in-memory SQLite. Включи позитивный тест, проверку ошибки 404 при отсутствии события и граничный случай переполнения лимита мест max_slots».*
* **Результат:** ИИ сгенерировал каркас файла `tests/test_api.py` с настройкой `StaticPool` для SQLite и переопределением зависимости `app.dependency_overrides[get_db]`.

## 2. Рефакторинг и документирование с помощью ИИ
ИИ использовался для добавления `docstrings` (описаний функций) и обновления устаревших вызовов Pydantic v1 (`event.dict()`) на современный синтаксис Pydantic v2 (`event.model_dump()`):

**Код ДО рефакторинга (`app/main.py`):**
```python
@app.post("/events/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = EventModel(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event