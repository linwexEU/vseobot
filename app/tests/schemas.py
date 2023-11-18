from pydantic import BaseModel, Field 


class STests(BaseModel): 
    code: str = Field(min_length=6, max_length=6) 
    name: str | None = ""




