from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Barber(Base):
    __tablename__ = "barbers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    appointments = relationship("Appointment", back_populates="barber")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    datetime = Column(DateTime)
    barber_id = Column(Integer, ForeignKey("barbers.id"))
    barber = relationship("Barber", back_populates="appointments") 