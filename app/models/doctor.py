"""医生模型"""
from sqlalchemy import Column, Integer, String, DateTime, Text, SmallInteger
from sqlalchemy.sql import func

from app.db.session import Base


class Doctor(Base):
    __tablename__ = "t_doctor"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    username = Column(String(50), unique=True, nullable=False, comment="登录账号")
    password = Column(String(100), nullable=False, comment="密码")
    real_name = Column(String(50), comment="医生姓名")
    department_id = Column(Integer, comment="所属科室ID")
    title = Column(String(50), comment="职称")
    specialty = Column(String(255), comment="擅长领域")
    introduction = Column(Text, comment="个人简介")
    avatar = Column(String(255), comment="头像路径")
    phone = Column(String(20), comment="手机号")
    status = Column(SmallInteger, default=1, comment="状态:1正常0禁用")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")