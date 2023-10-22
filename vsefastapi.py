from fastapi import FastAPI, Depends 
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from typing import Annotated
from func import FunctionBot
import uvicorn 


class Item(BaseModel): 
    code: Annotated[str, Field(min_length=6, max_length=6)]
    name: str | None = None


app = FastAPI() 
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_file_with_answer(item: Item) -> None:
    bot = FunctionBot(f"https://vseosvita.ua/test/go-settings?code={item.code}") 

    if item.name is None:
        bot.get_into_the_test()
    else: 
        bot.get_into_the_test(item.name)

    bot.pass_the_tests()


@app.get("/")
async def root() -> HTMLResponse: 
    with open("static/index.html", encoding="utf-8") as file:
        html_content = file.read() 
    return HTMLResponse(content=html_content)


@app.get("static/styles.css")
async def root_css() -> FileResponse: 
    return FileResponse("D:\Python\chromedriver\static\styles.css")


@app.post("/code")
async def code(file: Annotated[Item, Depends(get_file_with_answer)]) -> JSONResponse:  
    return JSONResponse(content={"Message": "Done!"})


@app.get("/question")
async def question_post() -> FileResponse: 
    return FileResponse(f"D:\\Python\\chromedriver\\vseobot-question.txt", filename="vseobot-question.txt", media_type="application/octet-stream")


if __name__ == "__main__": 
    uvicorn.run(app, host="127.0.0.1", port=8000)
