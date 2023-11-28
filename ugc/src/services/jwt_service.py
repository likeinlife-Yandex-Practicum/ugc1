from functools import lru_cache
from uuid import UUID

from fastapi import Request
import jwt

from src.core.config import settings
from src.core.exceptions import JWT_EXPIRED_EXCEPTION, JWT_INVALID_EXCEPTION


class JWTService:

    def __init__(self, public_key: str) -> None:
        self.public_key = public_key

    def get_user_id_from_token(self, access_token: str) -> UUID:
        """Get token from request, decode it and return user_id"""
        user_payload = self.decode_token(access_token)
        user_id = user_payload.get('sub')
        return user_id

    def decode_token(self, token: str) -> dict:
        """Decode any jwt token"""
        try:
            payload: dict = jwt.decode(token, self.public_key, algorithms=['RS256'])
        except jwt.ExpiredSignatureError:
            raise JWT_EXPIRED_EXCEPTION
        except jwt.InvalidTokenError:
            raise JWT_INVALID_EXCEPTION
        return payload


@lru_cache
def get_jwt_service() -> JWTService:
    with open(settings.rsa_public_path, 'r') as pub_obj:
        return JWTService(public_key=pub_obj.read())
