"""健康档案接口"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import require_roles, CurrentUser
from app.core.response import success
from app.db.session import get_db
from app.models.appointment import Appointment, HealthRecord
from app.models.doctor import Doctor
from app.models.doctor_consult import DoctorConsult
from app.models.user import User
from app.schemas.common import HealthRecordCreate, HealthRecordUpdate
from app.utils.helpers import format_datetime, format_date

router = APIRouter()


def _format_records(items, db):
    user_map = {u.id: u.real_name or u.username for u in db.query(User).all()}
    doctor_map = {d.id: d.real_name for d in db.query(Doctor).all()}
    return [{
        "id": r.id,
        "user_id": r.user_id,
        "user_name": user_map.get(r.user_id, ""),
        "doctor_id": r.doctor_id,
        "doctor_name": doctor_map.get(r.doctor_id, ""),
        "record_type": r.record_type or "",
        "diagnosis": r.diagnosis,
        "treatment": r.treatment,
        "prescription": r.prescription,
        "visit_date": format_date(r.visit_date),
        "create_time": format_datetime(r.create_time),
    } for r in items]


@router.get("/my")
def my_records(db: Session = Depends(get_db), current: CurrentUser = Depends(require_roles("user"))):
    """我的健康档案"""
    items = db.query(HealthRecord).filter(HealthRecord.user_id == current.user_id).order_by(HealthRecord.id.desc()).all()
    return success(_format_records(items, db))


@router.get("/doctor/patients")
def doctor_patients(db: Session = Depends(get_db), current: CurrentUser = Depends(require_roles("doctor"))):
    """医生查看患者档案"""
    items = db.query(HealthRecord).filter(HealthRecord.doctor_id == current.user_id).order_by(HealthRecord.id.desc()).all()
    return success(_format_records(items, db))


@router.get("/doctor/patient-options")
def doctor_patient_options(db: Session = Depends(get_db), current: CurrentUser = Depends(require_roles("doctor"))):
    """医生可选患者列表"""
    user_ids = set()
    for row in db.query(Appointment.user_id).filter(Appointment.doctor_id == current.user_id).distinct():
        user_ids.add(row.user_id)
    for row in db.query(DoctorConsult.user_id).filter(DoctorConsult.doctor_id == current.user_id).distinct():
        user_ids.add(row.user_id)
    for row in db.query(HealthRecord.user_id).filter(HealthRecord.doctor_id == current.user_id).distinct():
        user_ids.add(row.user_id)
    users = db.query(User).filter(User.id.in_(user_ids)).all() if user_ids else []
    return success([{"id": u.id, "name": u.real_name or u.username} for u in users])


@router.post("/doctor/create")
def doctor_create_record(
    req: HealthRecordCreate,
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(require_roles("doctor")),
):
    """医生创建患者档案"""
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        return success(None, "患者不存在")
    record = HealthRecord(
        user_id=req.user_id,
        doctor_id=current.user_id,
        record_type=req.record_type,
        diagnosis=req.diagnosis,
        treatment=req.treatment,
        prescription=req.prescription,
        visit_date=req.visit_date,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return success(_format_records([record], db)[0], "创建成功")


@router.put("/doctor/{record_id}")
def doctor_update_record(
    record_id: int,
    req: HealthRecordUpdate,
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(require_roles("doctor")),
):
    """医生更新患者档案"""
    record = db.query(HealthRecord).filter(
        HealthRecord.id == record_id,
        HealthRecord.doctor_id == current.user_id,
    ).first()
    if not record:
        return success(None, "档案不存在或无权限")
    if req.record_type is not None:
        record.record_type = req.record_type
    if req.diagnosis is not None:
        record.diagnosis = req.diagnosis
    if req.treatment is not None:
        record.treatment = req.treatment
    if req.prescription is not None:
        record.prescription = req.prescription
    if req.visit_date is not None:
        record.visit_date = req.visit_date
    db.commit()
    db.refresh(record)
    return success(_format_records([record], db)[0], "更新成功")


@router.delete("/doctor/{record_id}")
def doctor_delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current: CurrentUser = Depends(require_roles("doctor")),
):
    """医生删除患者档案"""
    record = db.query(HealthRecord).filter(
        HealthRecord.id == record_id,
        HealthRecord.doctor_id == current.user_id,
    ).first()
    if not record:
        return success(None, "档案不存在或无权限")
    db.delete(record)
    db.commit()
    return success(None, "删除成功")