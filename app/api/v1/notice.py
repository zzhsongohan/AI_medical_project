"""系统公告接口"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import require_roles, CurrentUser
from app.core.response import success, page_result
from app.db.session import get_db
from app.models.article import Notice
from app.schemas.common import NoticeCreate
from app.utils.helpers import format_datetime

router = APIRouter()

@router.get("/list")
def list_notices(db: Session = Depends(get_db)):
    """公告列表（公开）"""
    items = db.query(Notice).filter(Notice.status == 1).order_by(Notice.id.desc()).all()
    data = [{"id": n.id, "title": n.title, "content": n.content, "create_time": format_datetime(n.create_time)} for n in items]
    return success(data)


@router.get("/admin/list")
def admin_list_notices(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = Query(""),
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
):
    """公告管理列表（管理员）"""
    q = db.query(Notice)
    kw = keyword.strip()
    if kw:
        q = q.filter((Notice.title.like(f"%{kw}%")) | (Notice.content.like(f"%{kw}%")))
    total = q.count()
    items = q.order_by(Notice.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    data = [{
        "id": n.id, "title": n.title, "content": n.content, "status": n.status,
        "create_time": format_datetime(n.create_time),
    } for n in items]
    return page_result(data, total, page, page_size)


@router.get("/{notice_id}")
def get_notice(notice_id: int, db: Session = Depends(get_db)):
    """公告详情"""
    notice = db.query(Notice).filter(Notice.id == notice_id, Notice.status == 1).first()
    return success({
        "id": notice.id, "title": notice.title, "content": notice.content,
        "create_time": format_datetime(notice.create_time),
    } if notice else None)


@router.post("/create")
def create_notice(req: NoticeCreate, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """创建公告"""
    notice = Notice(title=req.title, content=req.content, status=req.status)
    db.add(notice)
    db.commit()
    return success({"id": notice.id}, "创建成功")


@router.put("/{notice_id}")
def update_notice(notice_id: int, req: NoticeCreate, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """更新公告"""
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if notice:
        notice.title = req.title
        notice.content = req.content
        notice.status = req.status
        db.commit()
    return success(None, "更新成功")


@router.delete("/{notice_id}")
def delete_notice(notice_id: int, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """删除公告"""
    db.query(Notice).filter(Notice.id == notice_id).delete()
    db.commit()
    return success(None, "删除成功")