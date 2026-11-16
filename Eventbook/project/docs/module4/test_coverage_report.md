# Отчет о тестировании и покрытии кода (Test Coverage)

## 1. Инструментарий
* **Фреймворк тестирования:** `pytest` + `fastapi.testclient`
* **Измерение покрытия:** `pytest-cov` (`coverage.py`)
* **Изоляция БД:** Тесты запускаются на изолированной in-memory базе данных SQLite (`sqlite:///:memory:`), что гарантирует отсутствие побочных эффектов.

## 2. Покрытые сценарии (`tests/test_api.py`)
1. `test_create_event_success` — позитивный тест создания мероприятия.
2. `test_create_booking_success` — позитивный тест бронирования слота.
3. `test_create_booking_event_not_found` — негативный тест (попытка записи на несуществующий ID события, ожидание HTTP 404).
4. `test_create_booking_slots_exceeded` — граничный случай (запись при заполненном лимите `max_slots`, ожидание HTTP 400).
5. `test_create_booking_invalid_email` — негативный тест валидации входных данных Pydantic (ожидание HTTP 422).

## 3. Метрики покрытия (Coverage Summary)

```text
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
app/__init__.py       0      0   100%
app/database.py      11      4    64%   14-18 (переопределено в тестах)
app/main.py          32      2    94%   24, 52 (GET-списки)
app/models.py        18      0   100%
app/schemas.py       21      0   100%
-----------------------------------------------
TOTAL                82      6    93%