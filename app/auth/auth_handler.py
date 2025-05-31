import time
from typing import Dict

from app.core.config import settings
from jose import jwt

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "exp": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        # print(time.time())
        # print(decoded_token["exp"])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception as e:
        print(f"error--->{e}")
        return {}