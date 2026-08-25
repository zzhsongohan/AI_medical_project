"""预约与健康档案ORM模型"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, func
from app.db.session import Base


class Appointment(Base):
    """预约挂号表 t_appointment"""
    __tablename__ = "t_appointment"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, nullable=False, comment="患者ID - 逻辑外键t_user.id")
    doctor_id = Column(Integer, nullable=False, comment="医生ID - 逻辑外键t_doctor.id")
    department_id = Column(Integer, nullable=False, comment="科室ID - 逻辑外键t_department.id")
    visit_date = Column(Date, nullable=False, comment="就诊日期")
    time_slot = Column(String(20), nullable=False, comment="时段:上午/下午/晚上")
    status = Column(Integer, default=0, comment="状态:0待确认1已确认2已完成3已取消")
    remark = Column(String(255), comment="备注")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class HealthRecord(Base):
    """健康档案表 t_health_record"""
    __tablename__ = "t_health_record"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, nullable=False, comment="患者ID - 逻辑外键t_user.id")
    doctor_id = Column(Integer, comment="医生ID - 逻辑外键t_doctor.id")
    record_type = Column(String(50), comment="档案类型")
    diagnosis = Column(String(255), comment="诊断结果")
    treatment = Column(Text, comment="治疗方案")
    prescription = Column(Text, comment="处方")
    visit_date = Column(Date, comment="就诊日期")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")