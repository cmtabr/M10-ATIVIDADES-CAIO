from fastapi import FastAPI, Request, HTTPException, status, Depends, Response
from sqlalchemy import insert, select, update, delete
from typing import Annotated

from .config.database import conn

from .models.todo_table import TodoTable
from .models.user_table import UserTable

from .auth.jwt_bearer import jwtBearer
from .auth.jwt_handler import signJWT, decodeJWT

app = FastAPI()

@app.get('/')
async def home():
    return {"Hello": "World"}

@app.post('/api/login')
async def login(username: str, password: str, response: Response):
    try:
        query = select(UserTable).where(UserTable.name == username and UserTable.password == password)
        result = conn.execute(query).first()
        user_id, _, _, _ = result
        if not result:
            raise HTTPException(status_code=400, detail="User does not exist.")
        token = signJWT(user_id)
        print(token)
        response.set_cookie(key="token", value=token)
        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/api/todos')
async def get_todos(request: Request):
    token: str = request.cookies.get("token")
    if not jwtBearer.verify_jwt(token):
        raise HTTPException(status_code=400, detail="Unauthenticated")
    query = conn.execute(select(TodoTable))
    result = query.fetchall()
    todos = [todo for todo in result]
    return todos if todos else "No todos found."

@app.get('/api/todo/{id}')
async def get_todo(id: int):
    query = conn.execute(select(TodoTable).where(TodoTable.todoId == id))
    result = query.first()
    return result

@app.post('/api/create_todo')
async def create_todo(
    task: str,
    description: str,
    status: int,
    priority: int,
    request: Request
    ):
    token = request.cookies.get("token")
    try:
        payload = decodeJWT(token)
        userId = payload.get("sub")
        new_todo = insert(TodoTable).values(
            task=task,
            description=description,
            status=status,
            priority=priority,
            userId=userId
        )
        conn.execute(new_todo)
        conn.commit()
        return status.HTTP_200_OK
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
@app.post('/api/update/{id}')
async def update_task(
    id: int,
    task: str,
    description: str,
    status: int,
    priority: int,
    request: Request
    ):
    token = request.cookies.get("token")
    if not jwtBearer.verify_jwt(token):
        raise HTTPException(status_code=400, detail="Unauthenticated")
    try:
        conn.execute(update(TodoTable).where(TodoTable.todoId == id).values(
            task=task,
            description=description,
            status=status,
            priority=priority
        ))
        conn.commit()
        return status.HTTP_302_FOUND
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@app.delete('/api/delete/{id}')
async def delete_todo(id: int, request: Request):
    token = request.cookies.get("token")
    if not jwtBearer.verify_jwt(token):
        raise HTTPException(status_code=400, detail="Unauthenticated")
    try:
        conn.execute(delete(TodoTable).where(TodoTable.todoId == id))
        conn.commit()
        return status.HTTP_200_OK
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
