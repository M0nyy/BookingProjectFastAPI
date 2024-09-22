from app.dao.basedao import BaseDAO
from app.hotels.models import HotelTable
from app.database import async_session_maker
from sqlalchemy import select, and_, or_
from app.bookings.models import BookingsTable
from datetime import date
from sqlalchemy import select, and_, or_
from app.bookings.models import BookingsTable


class HotelsDAO(BaseDAO):
    model = HotelTable



    class HotelsDAO(BaseDAO):
        model = HotelTable

        @classmethod
        async def search_for_hotels(cls, location: str, date_from: date, date_to: date):
            async with async_session_maker() as session:
                # Подзапрос для поиска занятых комнат в указанный период
                subquery = select(BookingsTable.room_id).where(
                    or_(
                        and_(BookingsTable.date_from >= date_from, BookingsTable.date_from <= date_to),
                        and_(BookingsTable.date_from <= date_from, BookingsTable.date_to > date_from)
                    )
                ).subquery()

                # Основной запрос для поиска отелей по локации, где есть свободные комнаты
                query = select(cls.model).where(
                    and_(
                        cls.model.location == location,
                        cls.model.id.notin_(select(subquery.c.room_id))
                    )
                )

                result = await session.execute(query)
                return result.scalars().all()



