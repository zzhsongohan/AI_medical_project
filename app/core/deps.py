"""依赖注入模块 - 当前用户与角色守卫"""
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.models.doctor import Doctor
from app.models.admin import Admin

security = HTTPBearer(auto_error=False)


class CurrentUser:
    """当前登录用户信息"""
    def __init__(self, user_id: int, username: str, role: str, obj=None):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.obj = obj


# 角色对应的模型映射
ROLE_MODEL_MAP = {
    "user": User,
    "doctor": Doctor,
    "admin": Admin
}

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> CurrentUser:
    """获取当前登录用户（需要登录才能访问的接口用这个）"""
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="未登录")
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌无效或已过期")
    user_id = payload.get("user_id")
    username = payload.get("sub")
    role = payload.get("role")
    if not user_id or not role:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌数据不完整")
    # ==== 新增：根据用户角色查用户对象
    model = ROLE_MODEL_MAP.get(role)
    obj = None
    if model:
        obj = db.query(model).filter(model.id == user_id).first()
    return CurrentUser(user_id=user_id, username=username, role=role,obj=obj)


def require_roles(*roles: str):
    """角色守卫 - 校验当前用户角色是否有权限"""
    def role_checker(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="权限不足")
        return current
    return role_checker