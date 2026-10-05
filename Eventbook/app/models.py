from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class EventModel(Base):
  __tablename__ = "events"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, nullable=False)
  description = Column(String, nullable=True)
  event_time = Column(DateTime, nullable=False)
  max_slots = Column(Integer, default=10)

  bookings = relationship("BookingModel", back_populates="event")


class BookingModel(Base):
  __tablename__ = "bookings"

  id = Column(Integer, primary_key=True, index=True)
  event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
  client_name = Column(String, nullable=False)
  client_email = Column(String, nullable=False)

  event = relationship("EventModel", back_populates="bookings")
