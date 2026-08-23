from datetime import timedelta, datetime
from typing import Optional

from jose import jwt, JWTError
from starlette.middleware.errors import JS

from app.core.config import settings


def create_access_token(data:dict,expires_delta:Optional[timedelta] = None) -> str:
    #创建JWT访问令牌
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.jwt_expire_minutes))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.jwt_secret_key,algorithm=settings.jwt_algorithm)

def decode_access_token(token:str) -> Optional[dict]:
    """解码JWT令牌"""
    try:
        payload = jwt.decode(token,settings.jwt_secret_key,algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None

def verify_password(plain_password: str, stored_password: str) -> bool:
    """验证密码（明文比对）"""
    return plain_password == stored_password
