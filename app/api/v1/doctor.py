"""医生管理接口"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import require_roles, CurrentUser
from app.core.response import success, page_result
from app.db.session import get_db
from app.models.doctor import Doctor
from app.models.department import Department
from app.models.appointment import Appointment, HealthRecord
from app.models.doctor_consult import DoctorConsult, DoctorReply
from app.schemas.common import DoctorCreate, DoctorUpdate
from app.utils.helpers import format_datetime

router = APIRouter()


def _doctor_to_dict(doctor: Doctor, dept_map: dict) -> dict:
    return {
        "id": doctor.id,
        "username": doctor.username,
        "real_name": doctor.real_name,
        "department_id": doctor.department_id,
        "department_name": dept_map.get(doctor.department_id, ""),
        "title": doctor.title,
        "specialty": doctor.specialty,
        "introduction": doctor.introduction,
        "avatar": doctor.avatar,
        "phone": doctor.phone,
        "status": doctor.status,
        "create_time": format_datetime(doctor.create_time),
    }


@router.get("/list")
def list_doctors(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = Query(""),
    department_id: int = Query(None),
    db: Session = Depends(get_db),
):
    """医生列表（公开，患者可选医生）"""
    q = db.query(Doctor).filter(Doctor.status == 1)
    if keyword:
        q = q.filter(Doctor.real_name.contains(keyword) | Doctor.specialty.contains(keyword))
    if department_id:
        q = q.filter(Doctor.department_id == department_id)
    total = q.count()
    items = q.order_by(Doctor.id).offset((page - 1) * page_size).limit(page_size).all()
    dept_map = {d.id: d.name for d in db.query(Department).all()}
    data = [_doctor_to_dict(d, dept_map) for d in items]
    return page_result(data, total, page, page_size)


@router.get("/admin/list")
def admin_list_doctors(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = Query(""),
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
):
    """医生管理列表（管理员）"""
    q = db.query(Doctor)
    if keyword:
        q = q.filter(
            Doctor.username.contains(keyword)
            | Doctor.real_name.contains(keyword)
            | Doctor.phone.contains(keyword)
            | Doctor.title.contains(keyword)
        )
    total = q.count()
    items = q.order_by(Doctor.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    dept_map = {d.id: d.name for d in db.query(Department).all()}
    data = [_doctor_to_dict(d, dept_map) for d in items]
    return page_result(data, total, page, page_size)


@router.post("/create")
def create_doctor(
    req: DoctorCreate,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
):
    """管理员创建医生"""
    if req.password != req.confirm_password:
        raise HTTPException(status_code=400, detail="两次密码输入不一致")
    existing = db.query(Doctor).filter(Doctor.username == req.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    doctor = Doctor(
        username=req.username,
        password=req.password,
        real_name=req.real_name,
        department_id=req.department_id,
        title=req.title,
        specialty=req.specialty,
        introduction=req.introduction,
        phone=req.phone,
        status=req.status,
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    dept_map = {d.id: d.name for d in db.query(Department).all()}
    return success(_doctor_to_dict(doctor, dept_map), "创建成功")


@router.put("/{doctor_id}")
def update_doctor(
    doctor_id: int,
    req: DoctorUpdate,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
):
    """管理员更新医生"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="医生不存在")
    if req.password:
        if not req.confirm_password:
            raise HTTPException(status_code=400, detail="请填写确认密码")
        if req.password != req.confirm_password:
            raise HTTPException(status_code=400, detail="两次密码输入不一致")
        doctor.password = req.password
    if req.real_name is not None:
        doctor.real_name = req.real_name
    if req.department_id is not None:
        doctor.department_id = req.department_id
    if req.title is not None:
        doctor.title = req.title
    if req.specialty is not None:
        doctor.specialty = req.specialty
    if req.introduction is not None:
        doctor.introduction = req.introduction
    if req.phone is not None:
        doctor.phone = req.phone
    if req.status is not None:
        doctor.status = req.status
    db.commit()
    db.refresh(doctor)
    dept_map = {d.id: d.name for d in db.query(Department).all()}
    return success(_doctor_to_dict(doctor, dept_map), "更新成功")


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
):
    """管理员删除医生（同时清理关联数据）"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="医生不存在")

    consult_ids = [c.id for c in db.query(DoctorConsult).filter(DoctorConsult.doctor_id == doctor_id).all()]
    if consult_ids:
        db.query(DoctorReply).filter(DoctorReply.consult_id.in_(consult_ids)).delete(synchronize_session=False)
        db.query(DoctorConsult).filter(DoctorConsult.doctor_id == doctor_id).delete(synchronize_session=False)

    db.query(Appointment).filter(Appointment.doctor_id == doctor_id).delete(synchronize_session=False)
    db.query(HealthRecord).filter(HealthRecord.doctor_id == doctor_id).delete(synchronize_session=False)

    db.delete(doctor)
    db.commit()
    return success(None, "删除成功")


@router.put("/{doctor_id}/status")
def toggle_doctor_status(
    doctor_id: int,
    status: int,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
):
    """切换医生状态"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="医生不存在")
    doctor.status = status
    db.commit()
    return success(None, "状态更新成功")