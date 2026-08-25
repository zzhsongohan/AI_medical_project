from datetime import date
from typing import Optional, List

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(...,description="用户名")
    password: str = Field(...,description="密码")
    role: str = Field(...,description="角色: user/doctory/admin")


class RegisterRequest(BaseModel):
    """注册请求 - 患者注册"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=50, description="密码")
    confirm_password: str = Field(..., description="确认密码")
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")

class TokenResponse(BaseModel):
    """登录/注册成功返回"""
    access_token: str
    token_type:str = "bearer"
    role: str
    user_id: int
    username: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None

class PasswordChangeRequest(BaseModel):
    """修改密码请求"""
    old_password: str
    new_password: str


class ProfileUpdateRequest(BaseModel):
    """更新个人资料"""
    nickname: Optional[str] = None
    real_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[int] = None
    age: Optional[int] = None
    allergy_history: Optional[str] = None   # 过敏史（用户专属）
    title: Optional[str] = None              # 职称（医生专属）
    specialty: Optional[str] = None          # 擅长（医生专属）
    introduction: Optional[str] = None       # 简介（医生专属）


class UserCreate(BaseModel):
    """管理员创建用户"""
    username: str
    password: str
    confirm_password: str
    real_name: Optional[str] = None
    gender: int = 1
    age: Optional[int] = None
    phone: Optional[str] = None
    allergy_history: Optional[str] = None
    status: int = 1

class UserUpdate(BaseModel):
    """管理员更新用户"""
    real_name: Optional[str] = None
    gender: Optional[int] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    allergy_history: Optional[str] = None
    status: Optional[int] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None

class DoctorCreate(BaseModel):
    """管理员创建医生"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)
    real_name: str = Field(..., min_length=1, max_length=50)
    department_id: Optional[int] = None
    title: Optional[str] = None
    specialty: Optional[str] = None
    introduction: Optional[str] = None
    phone: Optional[str] = None
    status: int = 1

class DoctorUpdate(BaseModel):
    """管理员更新医生"""
    real_name: Optional[str] = None
    department_id: Optional[int] = None
    title: Optional[str] = None
    specialty: Optional[str] = None
    introduction: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[int] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None

class DepartmentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    sort_order: int = 0

class ChatRequest(BaseModel):
    """发送问诊信息"""
    session_id: Optional[int] = None
    message: str = Field(..., min_length=1)

class GraphQueryRequest(BaseModel):
    """知识图谱查询"""
    symptoms: List[str] = Field(default_factory=list)  # 症状列表
    disease: Optional[str] = None   # 疾病名
    entity: Optional[str] = None    # 实体名

class DoctorConsultCreate(BaseModel):
    """发起医生查询"""
    doctor_id: Optional[int] = None
    chief_complaint: str

class DoctorReplyCreate(BaseModel):
    """医生回复"""
    consult_id: int   # 咨询ID
    content: str      # 回复内容

class AppointmentCreate(BaseModel):
    """提交预约"""
    doctor_id: int
    department_id: int
    visit_date: date
    time_slot: str
    remark: Optional[str] = None


class HealthRecordCreate(BaseModel):
    """健康档案创建"""
    user_id: int
    record_type: str
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    prescription: Optional[str] = None
    visit_date: Optional[date] = None


class HealthRecordUpdate(BaseModel):
    """修改健康档案"""
    record_type: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    prescription: Optional[str] = None
    visit_date: Optional[date] = None


class ArticleCreate(BaseModel):
    """文章创建"""
    title: str
    category: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    status: int = 1


class NoticeCreate(BaseModel):
    """公告创建"""
    title: str
    content: str = ""
    status: int = 1