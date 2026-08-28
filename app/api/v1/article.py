"""健康科普文章接口"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import require_roles, CurrentUser
from app.core.response import success, page_result
from app.db.session import get_db
from app.models.article import Article
from app.schemas.common import ArticleCreate
from app.utils.helpers import format_datetime

router = APIRouter()


@router.get("/list")
def list_articles(page: int = 1, page_size: int = 10, category: str = "", db: Session = Depends(get_db)):
    """文章列表（公开）"""
    q = db.query(Article).filter(Article.status == 1)
    if category:
        q = q.filter(Article.category == category)
    total = q.count()
    items = q.order_by(Article.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    data = [{
        "id": a.id, "title": a.title, "category": a.category, "cover": a.cover,
        "summary": a.summary, "view_count": a.view_count,
        "create_time": format_datetime(a.create_time),
    } for a in items]
    return page_result(data, total, page, page_size)


@router.get("/admin/list")
def admin_list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = Query(""),
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
):
    """文章管理列表（管理员）"""
    q = db.query(Article)
    kw = keyword.strip()
    if kw:
        q = q.filter(
            (Article.title.like(f"%{kw}%"))
            | (Article.summary.like(f"%{kw}%"))
            | (Article.category.like(f"%{kw}%"))
        )
    total = q.count()
    items = q.order_by(Article.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    data = [{
        "id": a.id, "title": a.title, "category": a.category, "cover": a.cover,
        "summary": a.summary, "view_count": a.view_count, "status": a.status,
        "create_time": format_datetime(a.create_time),
    } for a in items]
    return page_result(data, total, page, page_size)


@router.get("/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
    """文章详情"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if article:
        article.view_count = (article.view_count or 0) + 1
        db.commit()
    return success({
        "id": article.id, "title": article.title, "category": article.category,
        "content": article.content, "view_count": article.view_count,
        "create_time": format_datetime(article.create_time),
    } if article else None)


@router.post("/create")
def create_article(req: ArticleCreate, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """创建文章"""
    article = Article(title=req.title, category=req.category, summary=req.summary, content=req.content, status=req.status)
    db.add(article)
    db.commit()
    return success({"id": article.id}, "创建成功")


@router.put("/{article_id}")
def update_article(article_id: int, req: ArticleCreate, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """更新文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if article:
        article.title = req.title
        article.category = req.category
        article.summary = req.summary
        article.content = req.content
        article.status = req.status
        db.commit()
    return success(None, "更新成功")


@router.delete("/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """删除文章"""
    db.query(Article).filter(Article.id == article_id).delete()
    db.commit()
    return success(None, "删除成功")