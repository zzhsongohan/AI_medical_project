"""AI问诊ORM模型"""
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.db.session import Base


class ConsultSession(Base):
    """AI问诊会话表 t_consult_session"""
    __tablename__ = "t_consult_session"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, nullable=False, comment="用户ID - 逻辑外键t_user.id")
    title = Column(String(200), default="新会话", comment="会话标题")
    message_count = Column(Integer, default=0, comment="消息数量")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")


class ConsultMessage(Base):
    """AI问诊消息表 t_consult_message"""
    __tablename__ = "t_consult_message"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    session_id = Column(Integer, nullable=False, comment="会话ID - 逻辑外键t_consult_session.id")
    role = Column(String(20), nullable=False, comment="角色:user/assistant")
    content = Column(Text, nullable=False, comment="消息内容")
    references_json = Column(Text, comment="引用来源JSON")
    graph_json = Column(Text, comment="图谱实体JSON")
    cost_time = Column(Integer, default=0, comment="耗时毫秒")
    create_time = Column(DateTime, server_default=func.now(), comment="创建时间")