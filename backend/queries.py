from database_init import engine, Base, session_factory
from models import User
from sqlalchemy import select


class AsyncORM:

    @staticmethod
    async def create_table():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_user(tg_id: int):
        async with session_factory() as session:
            user = User(id=tg_id, balance=0, auto_miner=0, click_size=1)
            session.add(user)
            await session.commit()

    @staticmethod
    async def get_user(tg_id: int):
        async with session_factory() as session:
            query = select(User).where(User.id == tg_id)
            res = await session.execute(query)
            result = res.scalars().first()
        return result

    @staticmethod
    async def update_balance(tg_id: int, clicks: int):
        async with session_factory() as session:
            query = select(User).where(User.id == tg_id)
            res = await session.execute(query)
            result = res.scalars().first()
            result.balance += clicks
            await session.commit()

    @staticmethod
    async def update_click_size(tg_id: int):
        async with session_factory() as session:
            query = select(User).where(User.id == tg_id)
            res = await session.execute(query)
            result = res.scalars().first()
            result.click_size += 5
            await session.commit()
        return result
