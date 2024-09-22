from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.orm import relationship


class UserTable(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    booking = relationship('BookingsTable', back_populates='user')  # user указывает на атрибут user из BookingTable

    def __str__(self):
        return f'User {self.email}'