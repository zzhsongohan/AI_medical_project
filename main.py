"""AI智能医疗问诊平台系统 - FastAPI应用入口"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.utils.validation import format_validation_errors


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时初始化目录"""
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(os.path.join(settings.upload_dir, "knowledge"), exist_ok=True)
    os.makedirs(os.path.join(settings.upload_dir, "avatar"), exist_ok=True)
    os.makedirs(settings.chroma_persist_dir, exist_ok=True)
    print(f"[启动] {settings.project_name} 服务已就绪")
    if not settings.dashscope_api_key:
        print("[警告] DASHSCOPE_API_KEY 未设置，LLM功能不可用")
    yield


app = FastAPI(
    title=settings.project_name,
    description="基于RAG+LangChain+Neo4j的AI智能医疗问诊平台",
    version="1.0.0",
    lifespan=lifespan,
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """统一 HTTP 异常响应格式"""
    detail = exc.detail
    if isinstance(detail, str):
        message = detail
    elif isinstance(detail, list):
        message = "；".join(str(item) for item in detail)
    else:
        message = str(detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": message, "data": None},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """统一参数校验错误为中文提示"""
    message = format_validation_errors(exc.errors())
    return JSONResponse(
        status_code=422,
        content={"code": 422, "message": message, "data": None},
    )

# CORS跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件挂载
if os.path.exists(settings.upload_dir):
    app.mount("/uploads33", StaticFiles(directory=settings.upload_dir), name="uploads")

from app.api.v1 import api_router
app.include_router(api_router)

@app.get("/")
async def root():
    """根路径"""
    return {"message": f"欢迎使用{settings.project_name}", "docs": "/docs"}


@app.get("/health")
async def health_check():
    """健康检查接口（Docker用）"""
    return {"status": "ok"}