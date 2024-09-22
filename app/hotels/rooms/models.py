from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import relationship



class RoomTable(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[str] = mapped_column(JSON, nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int] = mapped_column()

    hotel = relationship('HotelTable', back_populates='rooms')
    booking = relationship('BookingsTable', back_populates='room')

