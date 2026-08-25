"""知识库管理接口"""
import os
from fastapi import APIRouter, Depends, UploadFile, File, Query, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import require_roles, CurrentUser
from app.core.response import success, page_result
from app.db.session import get_db
from app.models.knowledge import KnowledgeFile, KnowledgeChunk
from app.services.rag_service import get_rag_service
from app.utils.helpers import save_upload_file, get_file_type, format_datetime

router = APIRouter()

def _vectorize_task(file_id: int):
    """后台向量化任务"""
    from app.db.session import SessionLocal
    db = SessionLocal()
    try:
        file_record = db.query(KnowledgeFile).filter(KnowledgeFile.id == file_id).first()
        if file_record:
            get_rag_service().process_file(db, file_record)
    finally:
        db.close()

@router.get("/list")
def list_files(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = Query(""),
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
):
    """知识库文件列表（支持按文件名、类型搜索）"""
    q = db.query(KnowledgeFile)
    kw = keyword.strip()
    if kw:
        q = q.filter(
            (KnowledgeFile.file_name.like(f"%{kw}%"))
            | (KnowledgeFile.file_type.like(f"%{kw}%"))
        )
    total = q.count()
    items = q.order_by(KnowledgeFile.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    data = [{
        "id": f.id, "file_name": f.file_name, "file_type": f.file_type,
        "file_size": f.file_size, "chunk_count": f.chunk_count,
        "vector_status": f.vector_status,
        "create_time": format_datetime(f.create_time),
    } for f in items]
    return page_result(data, total, page, page_size)

@router.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(require_roles("admin")),
):
    """上传知识库文件并自动向量化"""
    file_type = get_file_type(file.filename)
    if file_type == "unknown":
        return success(None, "不支持的文件类型，仅支持 txt/doc/pdf/markdown")
    content = await file.read()
    rel_path = save_upload_file(content, file.filename, "knowledge")
    abs_path = os.path.join(settings.upload_dir, "knowledge", os.path.basename(rel_path))
    record = KnowledgeFile(
        file_name=file.filename,
        file_type=file_type,
        file_size=len(content),
        file_path=abs_path.replace("\\", "/"),
        upload_by=current.user_id,
        upload_role=current.role,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    background_tasks.add_task(_vectorize_task, record.id)
    return success({"id": record.id, "file_name": record.file_name}, "上传成功，正在向量化处理")


@router.post("/{file_id}/revectorize")
def revectorize(file_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """重新向量化"""
    record = db.query(KnowledgeFile).filter(KnowledgeFile.id == file_id).first()
    if not record:
        return success(None, "文件不存在")
    background_tasks.add_task(_vectorize_task, file_id)
    return success(None, "已开始重新向量化")


@router.delete("/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """删除知识库文件"""
    record = db.query(KnowledgeFile).filter(KnowledgeFile.id == file_id).first()
    if record:
        get_rag_service().vector_store.delete_by_file_id(file_id)
        db.query(KnowledgeChunk).filter(KnowledgeChunk.file_id == file_id).delete()
        if os.path.exists(record.file_path):
            os.remove(record.file_path)
        db.delete(record)
        db.commit()
    return success(None, "删除成功")



