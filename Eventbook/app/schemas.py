from datetime import datetime
from pydantic import BaseModel, EmailStr


class EventCreate(BaseModel):
  title: str
  description: str | None = None
  event_time: datetime
  max_slots: int = 10


class EventResponse(EventCreate):
  id: int

  class Config:
    from_attributes = True


class BookingCreate(BaseModel):
  event_id: int
  client_name: str
  client_email: EmailStr


class BookingResponse(BookingCreate):
  id: int

  class Config:
    from_attributes = True
