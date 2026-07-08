import jwt
import bcrypt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from jwt.exceptions import InvalidTokenError
from datetime import timedelta, timezone, datetime
from typing import Optional
from src.domain.interfaces import TokenService, SecurityService

class SecurityServicesRepo(SecurityService):
    def hash_password(self, plain_password: str):
        password = plain_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password=password, salt=salt)
        return hashed.decode('utf-8')
    def verify_password(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


class TokenService(TokenService):
    def __init__(self, SECRET_KEY, algorithm, expire_token_time):
        self.secret_key = SECRET_KEY
        self.algorithm = algorithm
        self.expire_time = expire_token_time
    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        expire = expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=self.expire_time))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, self.algorithm)
    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username = payload.get("sub")
            if username is None:
                return None
            return username
        except ExpiredSignatureError:
            print("Token has expired")
            return None
        except DecodeError:
            print("Token is malformed or signature is invalid")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None