from app.database import async_session_maker
from sqlalchemy import select, insert


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)  # SELECT * FROM table_name
            res = await session.execute(query)  # Возвращается <sqlalchemy.engine.result.ChunkedIteratorResult object>
            return res.scalar_one_or_none()  # И нам с ним нужно поработать

    @classmethod
    async def find_all(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)  # SELECT * FROM table_name
            res = await session.execute(query)  # Возвращается <sqlalchemy.engine.result.ChunkedIteratorResult object>
            return res.scalars().all()  # И нам с ним нужно поработать

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

