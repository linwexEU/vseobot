from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer 
from sqlalchemy.orm import relationship 


class Tests(Base): 
    __tablename__ = "tests" 

    id = Column(Integer, primary_key=True, nullable=False) 
    user_id = Column(Integer)

