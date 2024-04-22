import time
import jwt
from decouple import config 

JWT_SECRET = config('SECRET')
JWT_ALGORITHM = config('ALGORITHM')

def token_response(token:str):
    return {
        "access token" : token
    }

def signJWT(userId : int):
    payload = { 
        "sub" : userId,
        "expires" : time.time() + 3000 
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token
    except jwt.ExpiredSignatureError:
        return f'Token expirado: {decode_token}'
    except jwt.DecodeError:
        return f'Erro no decode: {decode_token}'