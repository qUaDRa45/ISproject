from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from models import BookingModel, EventModel
from schemas import BookingCreate, BookingResponse, EventCreate, EventResponse
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Consulting Booking API", version="1.0.0")


@app.post("/events/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
  db_event = EventModel(**event.dict())
  db.add(db_event)
  db.commit()
  db.refresh(db_event)
  return db_event


@app.get("/events/", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
  return db.query(EventModel).all()


@app.post("/bookings/", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
  event = db.query(EventModel).filter(EventModel.id == booking.event_id).first()
  if not event:
    raise HTTPException(status_code=404, detail="Событие не найдено")

  # Считаем текущие записи
  current_bookings_count = (
      db.query(BookingModel)
      .filter(BookingModel.event_id == booking.event_id)
      .count()
  )
  if current_bookings_count >= event.max_slots:
    raise HTTPException(
        status_code=400, detail="Свободных мест на это событие больше нет"
    )

  db_booking = BookingModel(**booking.dict())
  db.add(db_booking)
  db.commit()
  db.refresh(db_booking)
  return db_booking


@app.get("/bookings/", response_model=list[BookingResponse])
def get_bookings(db: Session = Depends(get_db)):
  return db.query(BookingModel).all()
