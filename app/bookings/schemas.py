from pydantic import BaseModel, Field
from datetime import date


class BookingSchema(BaseModel):
    id: int = Field(..., ge=1, description='Айди записи')
    room_id: int = Field(..., ge=1, description='Айди забронированной комнаты')
    user_id: int = Field(..., ge=1, description='Айди юзера который забронировал комнату')
    date_from: date = Field(..., description='Дата от')
    date_to: date = Field(..., description='Дата до')
    price: int = Field(..., description='Цена за сутки')
    total_cost: int = Field(..., description='Итоговая цена')
    total_days: int = Field(..., description='Итого дней')