"""API v1 路由汇总"""
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.graph import router as graph_router
from app.api.v1.knowledge import router as knowledge_router
from app.api.v1.chat import router as chat_router
from app.api.v1.user import router as user_router
from app.api.v1.doctor import router as doctor_router
from app.api.v1.department import router as department_router
from app.api.v1.consult import router as consult_router
from app.api.v1.appointment import router as appointment_router
from app.api.v1.record import router as record_router
from app.api.v1.article import router as article_router
from app.api.v1.notice import router as notice_router
from app.api.v1.stat import router as stat_router
from app.api.v1.profile import router as profile_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router, prefix="/auth", tags=["认证"])

api_router.include_router(graph_router, prefix="/graph", tags=["知识图谱"])

api_router.include_router(knowledge_router,prefix="/knowledge",tags=["知识库文件"])

api_router.include_router(chat_router,prefix="/chat",tags=["AI问诊"])

api_router.include_router(user_router,prefix="/user",tags=["用户管理"])

api_router.include_router(department_router,prefix="/department",tags=["科室管理"])

api_router.include_router(doctor_router,prefix="/doctor",tags=["医生管理"])

api_router.include_router(appointment_router,prefix="/appointment",tags=["预约管理"])

api_router.include_router(consult_router,prefix="/consult",tags=["人工问诊"])

api_router.include_router(record_router,prefix="/record",tags=["健康档案"])

api_router.include_router(article_router,prefix="/article",tags=["健康科普文章"])

api_router.include_router(notice_router,prefix="/notice",tags=["系统公告"])

api_router.include_router(stat_router,prefix="/stat",tags=["数据统计"])

api_router.include_router(profile_router,prefix="/profile",tags=["个人信息"])