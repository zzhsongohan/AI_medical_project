"""通用工具函数"""
import os
import uuid
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

def save_upload_file(file_content: bytes, original_name: str, sub_dir: str = "") -> str:
    from app.core.config import settings
    #项目目录/uploads
    upload_base = settings.upload_dir
    target_dir = os.path.join(upload_base, sub_dir) if sub_dir else upload_base
    os.makedirs(target_dir, exist_ok=True)
    ext = os.path.splitext(original_name)[1]
    new_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(target_dir, new_name)
    with open(file_path, "wb") as f:
        f.write(file_content)
    rel_path = f"/uploads/{sub_dir}/{new_name}" if sub_dir else f"/uploads/{new_name}"
    return rel_path.replace("\\", "/")

def get_file_type(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    mapping = {".txt": "txt", ".md": "markdown", ".pdf": "pdf", ".doc": "doc", ".docx": "doc"}
    return mapping.get(ext, "unknown")