from fastapi import FastAPI 

from app.users.router import router as router_reg
from app.tests.router import router as router_tests


app = FastAPI() 


app.include_router(router_reg)
app.include_router(router_tests)


