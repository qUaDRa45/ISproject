@startuml
skinparam defaultTextAlignment center
autonumber

actor "Клиент" as Client
participant "Web-интерфейс\n(Фронтенд)" as Web
participant "Система (API)\n(Бэкенд)" as API
database "База данных\n(PostgreSQL/SQLite)" as DB

== Целевой процесс записи (To-Be) ==
Client -> Web: Открывает список доступных мероприятий/слотов
Web -> API: Запрос актуального расписания (GET /events/)
API -> DB: Выборка свободных слотов
DB --> API: Список событий
API --> Web: Отображение данных пользователю

Client -> Web: Выбирает событие и вводит контакты, нажимает "Записаться"
Web -> API: Отправка данных бронирования (POST /bookings/)
API -> DB: Проверка лимита мест (max_slots)
alt Места есть
    DB --> API: OK
    API -> DB: Сохранение записи
    API --> Web: Успешный ответ (201 Created)
    Web --> Client: Показ сообщения об успешной записи
else Места закончились
    DB --> API: Лимит исчерпан
    API --> Web: Ошибка (400 Bad Request)
    Web --> Client: Уведомление об отсутствии мест
end
@enduml