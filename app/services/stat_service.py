"""统计服务"""
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from datetime import datetime, timedelta, date

from app.models.user import User
from app.models.doctor import Doctor
from app.models.consult import ConsultSession
from app.models.appointment import Appointment, HealthRecord
from app.models.doctor_consult import DoctorConsult
from app.models.knowledge import KnowledgeFile
from app.models.article import Article


class StatService:
    """数据统计服务"""

    @staticmethod
    def overview(db: Session) -> dict:
        """管理员统计概览"""
        return {
            "user_count": db.query(func.count(User.id)).scalar() or 0,
            "doctor_count": db.query(func.count(Doctor.id)).scalar() or 0,
            "consult_count": db.query(func.count(ConsultSession.id)).scalar() or 0,
            "appointment_count": db.query(func.count(Appointment.id)).scalar() or 0,
            "knowledge_count": db.query(func.count(KnowledgeFile.id)).scalar() or 0,
            "article_count": db.query(func.count(Article.id)).scalar() or 0,
        }

    @staticmethod
    def doctor_overview(db: Session, doctor_id: int) -> dict:
        """医生工作台统计概览"""
        today = date.today()
        pending_consults = db.query(func.count(DoctorConsult.id)).filter(
            or_(DoctorConsult.doctor_id == doctor_id, DoctorConsult.doctor_id.is_(None)),
            DoctorConsult.status == 0,
        ).scalar() or 0
        today_appointments = db.query(func.count(Appointment.id)).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.visit_date == today,
        ).scalar() or 0
        replied_consults = db.query(func.count(DoctorConsult.id)).filter(
            DoctorConsult.doctor_id == doctor_id,
            DoctorConsult.status == 1,
        ).scalar() or 0

        patient_ids = set()
        for row in db.query(HealthRecord.user_id).filter(HealthRecord.doctor_id == doctor_id).distinct():
            patient_ids.add(row[0])
        for row in db.query(Appointment.user_id).filter(Appointment.doctor_id == doctor_id).distinct():
            patient_ids.add(row[0])
        for row in db.query(DoctorConsult.user_id).filter(DoctorConsult.doctor_id == doctor_id).distinct():
            patient_ids.add(row[0])

        return {
            "pending_consults": pending_consults,
            "today_appointments": today_appointments,
            "total_patients": len(patient_ids),
            "replied_consults": replied_consults,
        }

    @staticmethod
    def user_overview(db: Session, user_id: int) -> dict:
        """用户个人统计概览"""
        return {
            "consult_count": db.query(func.count(DoctorConsult.id)).filter(
                DoctorConsult.user_id == user_id
            ).scalar() or 0,
            "appointment_count": db.query(func.count(Appointment.id)).filter(
                Appointment.user_id == user_id
            ).scalar() or 0,
            "record_count": db.query(func.count(HealthRecord.id)).filter(
                HealthRecord.user_id == user_id
            ).scalar() or 0,
            "chat_count": db.query(func.count(ConsultSession.id)).filter(
                ConsultSession.user_id == user_id
            ).scalar() or 0,
        }

    @staticmethod
    def consult_trend(db: Session, days: int = 7) -> list:
        """问诊趋势（近N天）"""
        result = []
        for i in range(days - 1, -1, -1):
            day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            count = db.query(func.count(ConsultSession.id)).filter(
                func.date(ConsultSession.create_time) == day
            ).scalar() or 0
            result.append({"date": day, "count": count})
        return result

    @staticmethod
    def appointment_by_department(db: Session) -> list:
        """科室预约分布"""
        from app.models.department import Department
        rows = db.query(
            Department.name,
            func.count(Appointment.id).label("count"),
        ).join(Appointment, Appointment.department_id == Department.id, isouter=True).group_by(Department.id).all()
        return [{"name": r[0], "value": r[1]} for r in rows]

    @staticmethod
    def user_growth(db: Session, days: int = 7) -> list:
        """用户增长趋势"""
        result = []
        for i in range(days - 1, -1, -1):
            day = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            count = db.query(func.count(User.id)).filter(
                func.date(User.create_time) == day
            ).scalar() or 0
            result.append({"date": day, "count": count})
        return result

    @staticmethod
    def knowledge_type_distribution(db: Session) -> list:
        """知识库文件类型分布"""
        rows = db.query(
            KnowledgeFile.file_type,
            func.count(KnowledgeFile.id).label("count"),
        ).group_by(KnowledgeFile.file_type).all()
        return [{"name": r[0], "value": r[1]} for r in rows]