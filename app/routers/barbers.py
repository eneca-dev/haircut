from fastapi import APIRouter, HTTPException
from ..database import supabase
from ..schemas import schemas
from typing import List

router = APIRouter(
    prefix="/barbers",
    tags=["barbers"]
)

@router.post("/", response_model=schemas.Barber)
def create_barber(barber: schemas.BarberCreate):
    result = supabase.table('barbers').insert({
        'name': barber.name
    }).execute()
    return result.data[0]

@router.get("/", response_model=List[schemas.Barber])
def read_barbers():
    result = supabase.table('barbers').select("*").execute()
    return result.data

@router.get("/{barber_id}", response_model=schemas.Barber)
def read_barber(barber_id: int):
    result = supabase.table('barbers').select("*").eq('id', barber_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Мастер не найден")
    return result.data[0]

@router.get("/{barber_id}/appointments", response_model=List[schemas.Appointment])
def read_barber_appointments(barber_id: int):
    # Сначала проверяем существование мастера
    barber = supabase.table('barbers').select("*").eq('id', barber_id).execute()
    if not barber.data:
        raise HTTPException(status_code=404, detail="Мастер не найден")
    
    # Получаем все записи мастера
    result = supabase.table('appointments').select("*").eq('barber_id', barber_id).execute()
    return result.data 