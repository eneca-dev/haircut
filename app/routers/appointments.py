from fastapi import APIRouter, HTTPException
from ..database import supabase
from ..schemas import schemas
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"]
)

@router.post("/", response_model=schemas.Appointment)
def create_appointment(appointment: schemas.AppointmentCreate):
    # Проверяем существование мастера
    barber = supabase.table('barbers').select("*").eq('id', appointment.barber_id).execute()
    if not barber.data:
        raise HTTPException(status_code=404, detail="Мастер не найден")
    
    # Проверяем, не занято ли это время
    existing = supabase.table('appointments').select("*")\
        .eq('barber_id', appointment.barber_id)\
        .eq('datetime', appointment.datetime.isoformat())\
        .execute()
    
    if existing.data:
        raise HTTPException(status_code=400, detail="Это время уже занято")
    
    # Создаем запись
    appointment_data = {
        'customer_name': appointment.customer_name,
        'datetime': appointment.datetime.isoformat(),
        'barber_id': appointment.barber_id
    }
    
    result = supabase.table('appointments').insert(appointment_data).execute()
    
    return result.data[0]

@router.get("/", response_model=List[schemas.Appointment])
def read_appointments():
    result = supabase.table('appointments').select("*").execute()
    return result.data

@router.get("/{appointment_id}", response_model=schemas.Appointment)
def read_appointment(appointment_id: int):
    result = supabase.table('appointments').select("*").eq('id', appointment_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return result.data[0]

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int):
    result = supabase.table('appointments').delete().eq('id', appointment_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return {"message": "Запись успешно удалена"} 