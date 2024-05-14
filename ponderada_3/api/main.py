from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from sqlalchemy import insert, select, update, delete

from .database import conn, session, Todos, Users
from .models import Todo, User

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield session
    except:
        session.rollback()
        ValueError("Database connection failed")
    finally:
        session.close_all()

app = FastAPI(lifespan=lifespan)

@app.post("/api/v1/signup", tags=["Entrance"])
async def signup(user: User):
    try:
        query = insert(Users).values(
            name=user.name,
            email=user.email,
            password=user.password
        )
        conn.execute(query)
        conn.commit()
        return status.HTTP_201_CREATED
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/login", tags=["Entrance"])
async def login(name: str, password: str):
    try:
        query = select(Users).where(Users.name == name and Users.password == password)
        result = conn.execute(query).first()
        if not result:
            raise HTTPException(status_code=400, detail="User does not exist.")
        return status.HTTP_200_OK
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/todo", tags=["To-Do"])
async def create_todo(todo: Todo):
    try: 
        query = insert(Todos).values(
            title=todo.title,
            description=todo.description,
            done=todo.done,
            user_id=todo.user_id
        )
        conn.execute(query)
        conn.commit()
        return status.HTTP_201_CREATED
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    
@app.get("/api/v1/todo/{id}", tags=["To-Do"])
async def read_single_todo(todo_id: int):
    try:
        query = select(Todos).where(Todos.id == todo_id)
        result = conn.execute(query).first()
        if not result:
            return status.HTTP_204_NO_CONTENT
        return result
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/todo", tags=["To-Do"])
async def read_all_todos():
    try:
        query = conn.execute(select(Todos))
        result = query.fetchall()
        todos = [{"task": todo[1], "description": todo[2], "status": todo[3], "priority": todo[4]} for todo in result]
        if todos == []:
            return status.HTTP_204_NO_CONTENT
        return todos
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@app.put("/api/v1/todo", tags=["To-Do"])
async def update_item(todo: Todo, todo_id: int):
    try: 
        query = update(Todos).where(Todos.id == todo_id).values(
            title=todo.title,
            description=todo.description,
            done=todo.done,
            user_id=todo.user_id
        )
        conn.execute(query)
        conn.commit()
        return status.HTTP_200_OK
    except Exception:
        return HTTPException(status_code=400, detail="Item not found")

@app.delete("/api/v1/todo", tags=["To-Do"])
async def delete_todo(todo: Todo):
    try: 
        query = delete(Todos).where(Todos.id == todo.id)
        conn.execute(query)
        conn.commit()
        return status.HTTP_200_OK
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
