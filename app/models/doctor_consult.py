"""人工问诊ORM模型"""
from sqlalchemy import Column, Integer, Text, DateTime, func
from app.db.session import Base


class DoctorConsult(Base):
    """人工问诊工单表 t_doctor_consult"""
    __tablename__ = "t_doctor_consult"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, nullable=False, comment="患者ID - 逻辑外键t_user.id")
    doctor_id = Column(Integer, comment="医生ID - 逻辑外键t_doctor.id，为空表示待分配")
    chief_complaint = Column(Text, nullable=False, comment="主诉")
    status = Column(Integer, default=0, comment="状态:0待回复1已回复")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class DoctorReply(Base):
    """医生回复表 t_doctor_reply"""
    __tablename__ = "t_doctor_reply"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    consult_id = Column(Integer, nullable=False, comment="工单ID - 逻辑外键t_doctor_consult.id")
    doctor_id = Column(Integer, nullable=False, comment="医生ID - 逻辑外键t_doctor.id")
    content = Column(Text, nullable=False, comment="回复内容")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")