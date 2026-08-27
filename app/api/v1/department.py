"""科室管理接口"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.deps import require_roles, CurrentUser
from app.core.response import success, page_result, error
from app.db.session import get_db
from app.models.department import Department
from app.models.doctor import Doctor
from app.schemas.common import DepartmentCreate
from app.utils.helpers import format_datetime

router = APIRouter()


def _get_doctor_count_map(db: Session) -> dict:
    rows = (
        db.query(Doctor.department_id, func.count(Doctor.id))
        .filter(Doctor.department_id.isnot(None), Doctor.status == 1)
        .group_by(Doctor.department_id)
        .all()
    )
    return {dept_id: count for dept_id, count in rows}


def _dept_to_dict(dept: Department, doctor_count_map: dict) -> dict:
    return {
        "id": dept.id,
        "name": dept.name,
        "description": dept.description,
        "sort_order": dept.sort_order or 0,
        "status": dept.status,
        "doctor_count": doctor_count_map.get(dept.id, 0),
        "create_time": format_datetime(dept.create_time),
    }


@router.get("/list")
def list_departments(db: Session = Depends(get_db)):
    """科室列表（公开）"""
    items = db.query(Department).filter(Department.status == 1).order_by(Department.sort_order).all()
    doctor_count_map = _get_doctor_count_map(db)
    data = [_dept_to_dict(d, doctor_count_map) for d in items]
    return success(data)


@router.get("/admin/list")
def admin_list_departments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = Query(""),
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
):
    """科室管理列表（管理员）"""
    q = db.query(Department)
    kw = keyword.strip()
    if kw:
        q = q.filter(
            (Department.name.like(f"%{kw}%")) | (Department.description.like(f"%{kw}%"))
        )
    total = q.count()
    items = (
        q.order_by(Department.sort_order, Department.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    doctor_count_map = _get_doctor_count_map(db)
    data = [_dept_to_dict(d, doctor_count_map) for d in items]
    return page_result(data, total, page, page_size)


@router.post("/create")
def create_department(req: DepartmentCreate, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """创建科室"""
    name = req.name.strip()
    if not name:
        return error("科室名称不能为空")
    exists = db.query(Department).filter(Department.name == name).first()
    if exists:
        return error("科室名称已存在")
    dept = Department(name=name, description=req.description, sort_order=req.sort_order)
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return success({"id": dept.id}, "创建成功")


@router.put("/{dept_id}")
def update_department(dept_id: int, req: DepartmentCreate, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """更新科室"""
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        return error("科室不存在")
    name = req.name.strip()
    if not name:
        return error("科室名称不能为空")
    exists = db.query(Department).filter(Department.name == name, Department.id != dept_id).first()
    if exists:
        return error("科室名称已存在")
    dept.name = name
    dept.description = req.description
    dept.sort_order = req.sort_order
    db.commit()
    return success(None, "更新成功")


@router.delete("/{dept_id}")
def delete_department(dept_id: int, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """删除科室"""
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        return error("科室不存在")
    doctor_count = db.query(Doctor).filter(Doctor.department_id == dept_id).count()
    if doctor_count > 0:
        return error(f"该科室下还有 {doctor_count} 位医生，无法删除")
    db.delete(dept)
    db.commit()
    return success(None, "删除成功")