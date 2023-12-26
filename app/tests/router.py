from fastapi import APIRouter, Depends, Request, HTTPException, BackgroundTasks
from fastapi.templating import Jinja2Templates
from app.tests.dao import TestDAO
from app.users.dao import UserDAO
from app.function.fastfunc import get_id_test, get_text_from_file
from app.tasks.tasks_bot import get_question
from app.tests.schemas import STests
from app.users.models import Users
import os
from app.function.func import FunctionBot

from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/tests",
    tags=["vseobot test"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("")
async def root_test(request: Request, user: Users = Depends(get_current_user)): 
    user_name = user["Users"].email.split("@")[0]
    return templates.TemplateResponse(
        name="index.html", 
        context={"request": request, "user_name": user_name}
    )


@router.post("/function")
async def vseobot(data: STests, background_task: BackgroundTasks, user: Users = Depends(get_current_user)):
    user_id = await UserDAO.get_user_id(user["Users"].email)
    if user_id is None: 
        raise HTTPException(status_code=404)
    
    await TestDAO.add(user_id=user_id["id"])
    test_id = await get_id_test(user_id["id"])
    if len(test_id) == 2: 
         await TestDAO.delete_test(test_id[-2]["id"])
         os.remove(f"all_tests/vseobot-question{test_id[-2]['id']}.txt")

    background_task.add_task(get_question(code=data.code, name=data.name, test_id=test_id[-1]["id"]))



@router.get("/all_questions")
async def view_all_question(request: Request, user: Users = Depends(get_current_user)): 
    user_id = await UserDAO.get_user_id(user["Users"].email)
    if user_id is None: 
        raise HTTPException(status_code=404)
    
    test_id = await get_id_test(user_id["id"])
    
    if test_id:
        question = await get_text_from_file(test_id[-1]["id"])
    else: 
        question = [["Нету тестов =("]]

    return templates.TemplateResponse(
        name="question.html", 
        context={"request": request, "questions": question}
    )






