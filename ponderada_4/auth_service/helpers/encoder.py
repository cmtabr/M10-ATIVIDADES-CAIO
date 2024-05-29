import json
import jwt

JWT_SECRET = "supersecret"
JWT_ALGORITHM = "HS256"

def token_response(token: str):
    return json.dumps({"access token": token})

def encode(user_id: int) -> str:
    payload = { 
        "id" : user_id,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)
    return token_response(token)