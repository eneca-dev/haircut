from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import appointments, barbers

app = FastAPI(title="Haircut Booking API")

# Добавляем middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Указываем кодировку для ответов
@app.middleware("http")
async def add_charset_middleware(request, call_next):
    response = await call_next(request)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

app.include_router(appointments.router)
app.include_router(barbers.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Haircut Booking API"} 