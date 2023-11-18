from fastapi import APIRouter, Request, HTTPException, Response, status
from fastapi.templating import Jinja2Templates
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.schemas import SAuth

from app.users.dao import UserDAO


router = APIRouter(
    prefix="/auth", 
    tags=["Auth & User"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/reg")
async def root_reg(request: Request): 
    return templates.TemplateResponse(
        name="reg.html",
        context={"request": request}
    )


@router.get("/log")
async def root_log(request: Request): 
    return templates.TemplateResponse(
        name="auth.html",
        context={"request": request}
    )


@router.post("/reg_user")
async def registration_user(data: SAuth):
    email = data.email
    existing_user = await UserDAO.find_one_or_none(email=email)
    if existing_user: 
        raise HTTPException(status_code=409)
    hashed_password = get_password_hash(data.password)
    await UserDAO.add(email=email, hashed_password=hashed_password)


@router.post("/login_user")
async def login_user(response: Response, data: SAuth):
    user = await authenticate_user(data.email, data.password)
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user["Users"].id)})
    response.set_cookie("vseobot_access", access_token, httponly=True)
    return {"access_token": access_token}

