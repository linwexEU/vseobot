from sqlalchemy import select
from app.dao.base import BaseDao 
from app.database import async_session_maker 

from app.users.models import Users

class UserDAO(BaseDao): 
    model = Users


    @classmethod 
    async def get_user_id(cls, email): 
        async with async_session_maker() as session: 
            query = select(Users.id).select_from(Users).where(Users.email == email)
            result = await session.execute(query) 
            return result.mappings().one_or_none() 
    


