from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON

from app.database import Base
from sqlalchemy.orm import relationship




class HotelTable(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[str] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int] = mapped_column()

    rooms = relationship('RoomTable', back_populates='hotel')



