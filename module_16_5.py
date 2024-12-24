from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from pydantic import BaseModel

# uvicorn module_16_5:app --reload

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    username: str
    age: int

users: List[User] = [
    User(id=1, username="UrbanUser", age=24),
    User(id=2, username="UrbanTest", age=22),
    User(id=3, username="Capybara", age=60)
]

@app.get("/", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: Annotated[int, Path(ge=1)]):
    for user in users:
        if user.id == user_id:  
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail='User was not found')



@app.post("/user/{username}/{age}")
async def post_user(username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
                    age: Annotated[int, Path(ge=18, le=120, description="Enter age", example='24')]):
    user_id = max((i.id for i in users), default=0) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description="Enter ID", example='1')], 
                      username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanProfi")],
                      age: Annotated[int, Path(ge=18, le=120, description="Enter age", example='28')]):
    try:
        user = users[user_id-1]
        user.username = username
        user.age = age
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')
    return user


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description="Enter ID", example='2')]):
    for i, user in enumerate(users):
        if user.id == user_id:
            del_user = users.pop(i)
            return del_user
    raise HTTPException(status_code=404, detail='User was not found')

