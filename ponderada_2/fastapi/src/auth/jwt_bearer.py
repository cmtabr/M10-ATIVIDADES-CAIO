from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decodeJWT

class jwtBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Token inválido ou expirado.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Token inválido ou expirado.")
        
    def verify_jwt(self, jwttoken:str) -> bool:
        payload = decodeJWT(jwttoken)
        return payload if payload is True else "Token inválido ou expirado."