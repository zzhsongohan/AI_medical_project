"""API v1 路由汇总"""
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.graph import router as graph_router
from app.api.v1.knowledge import router as knowledge_router
from app.api.v1.chat import router as chat_router
from app.api.v1.user import router as user_router
from app.api.v1.doctor import router as doctor_router
from app.api.v1.department import router as department_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router, prefix="/auth", tags=["认证"])

api_router.include_router(graph_router, prefix="/graph", tags=["知识图谱"])

api_router.include_router(knowledge_router,prefix="/knowledge",tags=["知识库文件"])

api_router.include_router(chat_router,prefix="/chat",tags=["AI问诊"])

api_router.include_router(user_router,prefix="/user",tags=["用户管理"])

api_router.include_router(department_router,prefix="/department",tags=["科室管理"])

api_router.include_router(doctor_router,prefix="/doctor",tags=["医生管理"])