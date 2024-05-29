from fastapi import FastAPI, HTTPException
from sqlalchemy import select, insert, and_
from redis import Redis

from uuid import uuid4
from schemas.user import UserRequest
from models.user_table import conn, UserTable
from helpers.encoder import encode
from logs.logger import Logger

logger = Logger(name="auth_service").get_logger()

redis = Redis(host="redis", port=6379, db=0)

app = FastAPI()

@app.post("/user/signup", tags=["User"])
async def login(user_request: UserRequest):
    try:
        query = insert(UserTable).values(email=user_request.email, 
                                        password=user_request.password
                                    )
        result = conn.execute(query)
        if result:
            logger.info("Usuários cadastrado com sucesso, e-mail: %s", user_request.email)
            return {"Response": "Usuário cadastrado"}
    except Exception as e:
        logger.error("Error during signup for email: %s, Error: %s", user_request.email, str(e))
        return HTTPException(status_code=400, detail=str(e))

@app.post("/user/login", tags=["User"])
async def login_user(user_request: UserRequest):
    logger.info("Requisição de login feita pelo usuáriio: %s", user_request.email)
    try:
        query = select(UserTable).where(and_(
                                        UserTable.email == user_request.email, 
                                        UserTable.password == user_request.password
                                        )
                                    )
        result = conn.execute(query).fetchone()

        if not result:
            logger.warning("Credenciais inválidas para o usuário: %s", user_request.email)
            return HTTPException(status_code=400, detail="Credenciais inválidas")
        
        token = encode(result.id)
        auth_id = str(uuid4())
        redis.set(auth_id, token)
        
        return {"message": "Usuário loggado com sucesso", "auth_id": auth_id}
    except Exception as e:
        logger.error("Erro durante o login para o email: %s, Erro: %s", user_request.email, str(e))
        return HTTPException(status_code=400, detail=str(e))