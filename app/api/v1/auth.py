from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.response import success
from app.db import session
from app.db.session import get_db
from app.schemas.common import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/login")
def login(req:LoginRequest,db:Session=Depends(get_db)):
    """三角色登录"""
    result = AuthService.login(db,req)
    return success(result.model_dump())

@router.post("/register")
def register(req:RegisterRequest,db:Session=Depends(get_db)):
    """患者注册"""
    result = AuthService.register(db,req)
    return success(result.model_dump())