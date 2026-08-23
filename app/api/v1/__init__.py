"""API v1 路由汇总"""
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router, prefix="/auth", tags=["认证"])