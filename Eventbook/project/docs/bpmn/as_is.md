@startuml
skinparam defaultTextAlignment center
autonumber

actor "Клиент" as Client
participant "Администратор / \nСпециалист" as Admin
database "Блокнот / \nExcel-таблица" as Excel

== Текущий процесс записи (As-Is) ==
Client -> Admin: Пишет в мессенджер / звонит с запросом на консультацию
Admin -> Excel: Проверяет свободное время вручную (риск ошибок и накладок)
alt Время занято
    Admin --> Client: Сообщает об ошибке, предлагает другое время
    Client -> Admin: Выбирает новое время
end
Admin -> Excel: Записывает данные клиента вручную
Admin --> Client: Подтверждает запись текстовым сообщением
@enduml