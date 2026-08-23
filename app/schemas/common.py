from typing import Optional

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(...,description="用户名")
    password: str = Field(...,description="密码")
    role: str = Field(...,description="角色: user/doctory/admin")


class RegisterRequest(BaseModel):
    """注册请求 - 患者注册"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=50, description="密码")
    confirm_password: str = Field(..., description="确认密码")
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")

class TokenResponse(BaseModel):
    """登录/注册成功返回"""
    access_token: str
    role: str
    user_id: int
    username: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None