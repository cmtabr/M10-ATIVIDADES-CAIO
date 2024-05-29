import jwt

JWT_SECRET = "supersecret"
JWT_ALGORITHM = "HS256"

def decoder(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return {"id": decode_token}
    except jwt.DecodeError:
        return f'Erro no decode: {decode_token}'