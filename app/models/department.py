"""科室模型"""
from sqlalchemy import Column, Integer, String, DateTime, SmallInteger
from sqlalchemy.sql import func

from app.db.session import Base


class Department(Base):
    __tablename__ = "t_department"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="科室名称")
    description = Column(String(500), comment="科室描述")
    sort_order = Column(Integer, default=0, comment="排序")
    status = Column(SmallInteger, default=1, comment="状态")
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())