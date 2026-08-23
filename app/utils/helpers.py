"""通用工具函数"""
from datetime import datetime


def format_datetime(dt) -> str:
    """格式化日期时间为 YYYY-MM-DD HH:mm:ss"""
    if not dt:
        return ""
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return str(dt)


def format_date(dt) -> str:
    """格式化日期为 YYYY-MM-DD"""
    if not dt:
        return ""
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d")
    return str(dt)