from pydantic import BaseModel, EmailStr
from datetime import datetime

class Todo(BaseModel):
    """
    Essa classe define o modelo de dados para um to-do.
    """
    task: str 
    description: str 
    status: int 
    priority: int 
    deadline: datetime 
    class Config:
        json_schema_extra = {
            "example": {
                "task": "Teste",
                "description": "Teste",
                "status": 1,
                "priority": 1,
            }
        }