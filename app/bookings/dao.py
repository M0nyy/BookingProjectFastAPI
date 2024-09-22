# DAO - data access object
from datetime import date

from sqlalchemy import and_, func, insert, or_, select

from app.bookings.models import BookingsTable
from app.bookings.schemas import BookingSchema
from app.dao.basedao import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import RoomTable


class BookingDAO(BaseDAO):
    model = BookingsTable

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = (
                select(BookingsTable)
                .where(
                    and_(
                        BookingsTable.room_id == room_id,
                        or_(
                            and_(
                                BookingsTable.date_from >= date_from,
                                BookingsTable.date_from <= date_to,
                            ),
                            and_(
                                BookingsTable.date_from <= date_from,
                                BookingsTable.date_to > date_from,
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            get_rooms_left = (
                select(RoomTable.quantity - func.count(booked_rooms.c.room_id))
                .select_from(RoomTable)
                .join(
                    booked_rooms, booked_rooms.c.room_id == RoomTable.id, isouter=True
                )
                .where(RoomTable.id == room_id)
                .group_by(RoomTable.quantity, booked_rooms.c.room_id)
            )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()
            print(f"{rooms_left}")

            if rooms_left is not None and rooms_left > 0:  # Если есть свободные комнаты

                get_price = select(RoomTable.price).filter_by(
                    id=room_id
                )  # То для создания букинга нам не хватает только цены за номер, которую мы сами получаем
                price = await session.execute(get_price)
                price: int = price.scalar()

                add_booking = (
                    insert(BookingsTable)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(BookingsTable)
                )

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else:
                return None

    @classmethod
    async def delete(cls, booking):
        async with async_session_maker() as session:
            res = await session.delete(booking)
            if not res:
                return None
            else:
                await session.commit()
