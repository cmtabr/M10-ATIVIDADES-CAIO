from fastapi import FastAPI, Request, HTTPException, status, Header, Response, Depends
from sqlalchemy import insert, select, update, delete
import json
from pydantic import BaseModel


from .config.database import conn

from .models.todo_table import TodoTable
from .models.user_table import UserTable

from .auth.jwt_bearer import jwtBearer
from .auth.jwt_handler import signJWT, decodeJWT

class Todo(BaseModel):
    id: int
    task: str
    description: str
    status: int
    priority: int

app = FastAPI()

async def verify_token(x_token: str = Header(...)):
    if not jwtBearer.verify_jwt(jwtBearer, jwttoken=x_token):
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token

async def verify_key(x_key: str = Header(...)):
    if x_key != "token":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

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
        response.set_cookie(key="token", value=token)
        return token
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/api/todos', 
        dependencies=[Depends(verify_token), Depends(verify_key)],
        status_code=status.HTTP_200_OK,
        )
async def get_todos(request: Request):
    try:
        token = request.headers.get("x-token")
        userId = decodeJWT(token).get("sub")
        query = conn.execute(select(TodoTable).where(TodoTable.userId == userId))
        result = query.fetchall()
        todos = [{"task": todo[1], "description": todo[2], "status": todo[3], "priority": todo[4]} for todo in result]
        return todos
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@app.get('/api/find_todo', dependencies=[Depends(verify_token), Depends(verify_key)])
async def get_todo(id: int):
    try: 
        query = conn.execute(select(TodoTable).where(TodoTable.todoId == id))
        result = query.first()
        return {"task": result[1], "description": result[2], "status": result[3], "priority": result[4]}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@app.post('/api/create_todo', 
        dependencies=[Depends(verify_token), Depends(verify_key)],
        status_code=status.HTTP_200_OK)
async def create_todo(todo: Todo,
    request: Request
    ):
    try:
        token = request.headers.get("x-token")
        payload = decodeJWT(token)
        userId = payload.get("sub")
        new_todo = insert(TodoTable).values(
            task=todo.task,
            description=todo.description,
            status=todo.status,
            priority=todo.priority,
            userId=userId
        )
        conn.execute(new_todo)
        conn.commit()
        return {"message": "Todo created successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
@app.put('/api/update', 
        dependencies=[Depends(verify_token), Depends(verify_key)], 
        status_code=status.HTTP_200_OK)
async def update_task(
    todo: Todo,
    request: Request
    ):
    try:
        token = request.headers.get("x-token")
        payload = decodeJWT(token)
        userId = payload.get("sub")
        conn.execute(update(TodoTable).where(TodoTable.todoId == todo.id).values(
            task=todo.task,
            description=todo.description,
            status=todo.status,
            priority=todo.priority
        ))
        conn.commit()
        return {"message": "Todo updated successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@app.delete('/api/delete', 
            dependencies=[Depends(verify_token), Depends(verify_key)],
            status_code=status.HTTP_200_OK)
async def delete_todo(todo: Todo):
    try:
        conn.execute(delete(TodoTable).where(TodoTable.todoId == todo.id))
        conn.commit()
        return {"message": "Todo deleted successfully"}
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
