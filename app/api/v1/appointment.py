"""预约挂号接口"""
from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.deps import require_roles, CurrentUser
from app.core.response import success, page_result
from app.db.session import get_db
from app.models.appointment import Appointment
from app.models.user import User
from app.models.doctor import Doctor
from app.models.department import Department
from app.schemas.common import AppointmentCreate
from app.utils.helpers import format_datetime, format_date

router = APIRouter()


def _format_appts(items, db):
    user_map = {u.id: u.real_name or u.username for u in db.query(User).all()}
    doctor_map = {d.id: d.real_name for d in db.query(Doctor).all()}
    dept_map = {d.id: d.name for d in db.query(Department).all()}
    return [{
        "id": a.id, "user_id": a.user_id, "user_name": user_map.get(a.user_id, ""),
        "doctor_id": a.doctor_id, "doctor_name": doctor_map.get(a.doctor_id, ""),
        "department_id": a.department_id, "department_name": dept_map.get(a.department_id, ""),
        "visit_date": format_date(a.visit_date), "time_slot": a.time_slot,
        "status": a.status, "remark": a.remark,
        "create_time": format_datetime(a.create_time),
    } for a in items]


@router.post("/create")
def create_appointment(req: AppointmentCreate, db: Session = Depends(get_db), current: CurrentUser = Depends(require_roles("user"))):
    """创建预约"""
    appt = Appointment(
        user_id=current.user_id,
        doctor_id=req.doctor_id,
        department_id=req.department_id,
        visit_date=req.visit_date,
        time_slot=req.time_slot,
        remark=req.remark,
    )
    db.add(appt)
    db.commit()
    return success({"id": appt.id}, "预约成功")


@router.get("/my")
def my_appointments(db: Session = Depends(get_db), current: CurrentUser = Depends(require_roles("user"))):
    """我的预约"""
    items = db.query(Appointment).filter(Appointment.user_id == current.user_id).order_by(Appointment.id.desc()).all()
    return success(_format_appts(items, db))


@router.get("/doctor/my")
def doctor_appointments(db: Session = Depends(get_db), current: CurrentUser = Depends(require_roles("doctor"))):
    """医生的预约"""
    items = db.query(Appointment).filter(Appointment.doctor_id == current.user_id).order_by(Appointment.id.desc()).all()
    return success(_format_appts(items, db))


@router.get("/admin/list")
def admin_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = Query(""),
    department_id: int = Query(None),
    visit_date: date = Query(None),
    status: int = Query(None),
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
):
    """管理员预约列表"""
    q = db.query(Appointment)
    if keyword:
        q = (
            q.outerjoin(User, Appointment.user_id == User.id)
            .outerjoin(Doctor, Appointment.doctor_id == Doctor.id)
            .filter(
                or_(
                    User.username.contains(keyword),
                    User.real_name.contains(keyword),
                    Doctor.real_name.contains(keyword),
                    Appointment.remark.contains(keyword),
                )
            )
            .distinct()
        )
    if department_id is not None:
        q = q.filter(Appointment.department_id == department_id)
    if visit_date is not None:
        q = q.filter(Appointment.visit_date == visit_date)
    if status is not None:
        q = q.filter(Appointment.status == status)
    total = q.count()
    items = q.order_by(Appointment.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return page_result(_format_appts(items, db), total, page, page_size)


@router.delete("/admin/{appt_id}")
def admin_delete_appointment(
    appt_id: int,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
):
    """管理员删除预约记录"""
    appt = db.query(Appointment).filter(Appointment.id == appt_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="预约记录不存在")
    db.delete(appt)
    db.commit()
    return success(None, "删除成功")


@router.put("/{appt_id}/status")
def update_status(appt_id: int, status: int, db: Session = Depends(get_db), current: CurrentUser = Depends(require_roles("admin", "doctor"))):
    """更新预约状态"""
    appt = db.query(Appointment).filter(Appointment.id == appt_id).first()
    if appt:
        appt.status = status
        db.commit()
    return success(None, "状态更新成功")