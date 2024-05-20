from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class UserRequest(BaseModel):
    name: str
    email: str
    password: str

app = FastAPI()

def create_user(user_request: UserRequest) -> str:
    try:
        return "User created successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/user/signup", tags=["User"], status_code=201)
async def create_user_endpoint(user_request: UserRequest):
    try:
        response = create_user(user_request)
        return {"message": response}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

@app.post("/user/login", tags=["User"], status_code=200)
async def login_user():
    try:
        return {"message": "User logged in successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
