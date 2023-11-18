from pydantic import BaseModel, Field, EmailStr


class SAuth(BaseModel): 
    email: EmailStr
    password: str = Field(min_length=5)

