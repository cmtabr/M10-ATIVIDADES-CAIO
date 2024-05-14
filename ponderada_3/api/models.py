from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str

class Todo(BaseModel):
    title: str
    description: str
    done: int
    user_id: int
