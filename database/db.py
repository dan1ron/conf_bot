from async_lru import alru_cache
from typing import Optional, Union

from sqlalchemy import and_, func, or_, update, not_, delete, select, insert
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from database.models import User  # Link, Category


class Database:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, entry):
        try:
            self.session.add(entry)
            await self.session.commit()
            await self.session.refresh(entry)
        except IntegrityError as e:
            await self.session.rollback()
            raise e

    async def users_count(self) -> int:
        q = select([func.count(User.id)])
        return (await self.session.execute(q)).scalar()

    async def add_user(self, id_, username):
        await self.add(User(id=id_, username=username))
        self.get_users.cache_clear()
        self.get_user.cache_clear()


    @alru_cache(1024)
    async def get_user(self, id_: int) -> Optional[User]:
        q = select(User).where(User.id == id_)
        user = await self.session.execute(q)
        return user.scalar()

    @alru_cache(123)
    async def get_users(self):
        q = select(User)
        users = await self.session.scalars(q)
        return users.all()

    async def update_user_role(self, id_, role):
        q = update(User).where(User.id == id_).values(role=role)
        users = await self.session.scalars(q)
        self.get_user.cache_clear()
        return users.all()
