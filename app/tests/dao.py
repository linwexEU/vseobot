from sqlalchemy import delete, select
from app.tests.models import Tests
from app.dao.base import BaseDao 
from app.database import async_session_maker 


class TestDAO(BaseDao): 
    model = Tests

    @classmethod 
    async def get_user_tests(cls, user_id): 
        async with async_session_maker() as session: 
            query = select(Tests.id).select_from(cls.model).where(Tests.user_id == user_id) 
            result = await session.execute(query) 
            return result.mappings().all()
        
    @classmethod 
    async def delete_test(cls, test_id): 
        async with async_session_maker() as session: 
            query = delete(cls.model).where(Tests.id == test_id) 
            await session.execute(query) 
            await session.commit() 
            