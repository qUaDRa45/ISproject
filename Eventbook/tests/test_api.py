import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app

# Настройка тестовой БД в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# 1. Позитивный сценарий: создание мероприятия
def test_create_event_success():
    response = client.post(
        "/events/",
        json={
            "title": "Консультация по Python",
            "description": "Разбор архитектуры",
            "event_time": "2026-11-20T15:00:00",
            "max_slots": 2,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Консультация по Python"
    assert data["max_slots"] == 2
    assert "id" in data


# 2. Позитивный сценарий: успешная запись на мероприятие
def test_create_booking_success():
    event_res = client.post(
        "/events/",
        json={
            "title": "Воркшоп по Docker",
            "event_time": "2026-11-21T18:00:00",
            "max_slots": 5,
        },
    )
    event_id = event_res.json()["id"]

    booking_res = client.post(
        "/bookings/",
        json={
            "event_id": event_id,
            "client_name": "Иван Иванов",
            "client_email": "ivan@example.com",
        },
    )
    assert booking_res.status_code == 200
    assert booking_res.json()["client_email"] == "ivan@example.com"


# 3. Негативный сценарий: запись на несуществующее событие (404)
def test_create_booking_event_not_found():
    response = client.post(
        "/bookings/",
        json={
            "event_id": 999,
            "client_name": "Петр Петров",
            "client_email": "petr@example.com",
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Событие не найдено"


# 4. Негативный сценарий (граничный случай): превышение лимита мест (400)
def test_create_booking_slots_exceeded():
    event_res = client.post(
        "/events/",
        json={
            "title": "Индивидуальный разбор",
            "event_time": "2026-11-22T12:00:00",
            "max_slots": 1,
        },
    )
    event_id = event_res.json()["id"]

    # Первая запись проходит (1 из 1)
    first = client.post(
        "/bookings/",
        json={
            "event_id": event_id,
            "client_name": "Клиент 1",
            "client_email": "c1@example.com",
        },
    )
    assert first.status_code == 200

    # Вторая запись должна быть отклонена
    second = client.post(
        "/bookings/",
        json={
            "event_id": event_id,
            "client_name": "Клиент 2",
            "client_email": "c2@example.com",
        },
    )
    assert second.status_code == 400
    assert second.json()["detail"] == "Свободных мест на это событие больше нет"


# 5. Негативный сценарий: невалидный формат Email (422)
def test_create_booking_invalid_email():
    response = client.post(
        "/bookings/",
        json={
            "event_id": 1,
            "client_name": "Тест",
            "client_email": "not-an-email",
        },
    )
    assert response.status_code == 422