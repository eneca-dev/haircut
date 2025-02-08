from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BarberBase(BaseModel):
    name: str

class BarberCreate(BarberBase):
    pass

class Barber(BarberBase):
    id: int

class AppointmentBase(BaseModel):
    customer_name: str
    datetime: datetime
    barber_id: int

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int 