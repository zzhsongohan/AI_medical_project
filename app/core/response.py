"""统一响应格式"""
from typing import Any


def success(data: Any = None, message: str = "操作成功") -> dict:
    """成功响应"""
    return {"code": 200, "message": message, "data": data}


def error(message: str = "操作失败", code: int = 400) -> dict:
    """失败响应"""
    return {"code": code, "message": message, "data": None}


def page_result(items: list, total: int, page: int = 1, page_size: int = 10) -> dict:
    """分页响应"""
    return success({
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    })