import json
import jwt

JWT_SECRET = "supersecret"
JWT_ALGORITHM = "HS256"

def token_response(token: str):
    return json.dumps({"access token": token})

def signJWT(userId : int) -> str:
    payload = { 
        "sub" : userId,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token
    except jwt.DecodeError:
        return f'Erro no decode: {decode_token}'