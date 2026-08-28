"""数据统计接口"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import require_roles, CurrentUser
from app.core.response import success
from app.db.session import get_db
from app.services.stat_service import StatService

router = APIRouter()


@router.get("/overview")
def overview(db: Session = Depends(get_db), current: CurrentUser = Depends(require_roles("admin", "doctor"))):
    """统计概览（管理员/医生按角色返回不同数据）"""
    if current.role == "doctor":
        return success(StatService.doctor_overview(db, current.user_id))
    return success(StatService.overview(db))


@router.get("/user-overview")
def user_overview(db: Session = Depends(get_db), current: CurrentUser = Depends(require_roles("user"))):
    """用户个人统计概览"""
    return success(StatService.user_overview(db, current.user_id))


@router.get("/consult-trend")
def consult_trend(days: int = 7, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """问诊趋势"""
    return success(StatService.consult_trend(db, days))


@router.get("/appointment-dept")
def appointment_dept(db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """科室预约分布"""
    return success(StatService.appointment_by_department(db))


@router.get("/user-growth")
def user_growth(days: int = 7, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """用户增长"""
    return success(StatService.user_growth(db, days))


@router.get("/knowledge-type")
def knowledge_type(db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    """知识库类型分布"""
    return success(StatService.knowledge_type_distribution(db))