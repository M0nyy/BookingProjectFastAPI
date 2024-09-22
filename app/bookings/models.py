from datetime import date

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Date, Computed

from sqlalchemy.orm import relationship


class BookingsTable(Base):

    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_from: Mapped[date] = mapped_column(Date, nullable=False)
    date_to: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(Computed('(date_to - date_from) * price'))
    total_days: Mapped[int] = mapped_column(Computed('date_to - date_from'))

    user = relationship('UserTable', back_populates='booking')
    room = relationship('RoomTable', back_populates='booking')

    def __str__(self):
        return f'{self.id}, {self.date_from}, {self.date_to}'
