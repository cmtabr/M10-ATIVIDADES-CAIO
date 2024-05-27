from fastapi import FastAPI, HTTPException
from sqlalchemy import select, insert
from schemas.user import UserRequest
from models.user_table import conn, UserTable
from helpers.jwt_handler import signJWT

app = FastAPI()

@app.post("/user/signup", tags=["User"], status_code=201)
async def login(user_request: UserRequest):
    try:
        query = insert(UserTable).values(email=user_request.email, 
                                        password=user_request.password
                                    )
        result = conn.execute(query)
        if result:
            return {"Response": "Usuário cadastrado"}
    except Exception as e: 
        return HTTPException(status_code=400, detail=str(e))

@app.post("/user/login", tags=["User"], status_code=200)
async def login_user(user_request: UserRequest):
    try:
        query = select(UserTable).where(UserTable.email == user_request.email)
        result = conn.execute(query).fetchone()
        if result:
            token = signJWT(result.id)
            return {"message": "User logged in successfully", "token": token}
        else:
            raise HTTPException(status_code=400, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))