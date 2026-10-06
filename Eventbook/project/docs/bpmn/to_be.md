# Схема целевого процесса (To-Be)

Ниже представлена диаграмма целевого процесса с автоматической проверкой мест и сохранением в базу данных.

```mermaid
sequenceDiagram
    autonumber
    actor Client as Клиент
    participant Web as Web-интерфейс (Фронтенд)
    participant API as Система (API) (Бэкенд)
    participant DB as База данных (SQLite/PostgreSQL)
    
    Note over Client, DB: Целевой процесс записи (To-Be)
    Client->>Web: Открывает список доступных мероприятий
    Web->>API: Запрос расписания (GET /events/)
    API->>DB: Выборка свободных слотов
    DB-->>API: Список событий
    API-->>Web: Отображение данных пользователю
    
    Client->>Web: Выбирает событие, вводит контакты, нажимает «Записаться»
    Web->>API: Отправка данных (POST /bookings/)
    API->>DB: Проверка лимита мест (max_slots)
    alt Места есть
        DB-->>API: OK
        API->>DB: Сохранение записи
        API-->>Web: Успешный ответ (201 Created)
        Web-->>Client: Показ сообщения об успехе
    else Места закончились
        DB-->>API: Лимит исчерпан
        API-->>Web: Ошибка (400 Bad Request)
        Web-->>Client: Уведомление об отсутствии мест
    end
