"""个人中心接口"""
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, CurrentUser
from app.core.response import success
from app.core.security import verify_password
from app.db.session import get_db
from app.schemas.common import ProfileUpdateRequest, PasswordChangeRequest
from app.utils.helpers import save_upload_file, format_datetime

router = APIRouter()


@router.get("/info")
def get_profile(current: CurrentUser = Depends(get_current_user)):
    """获取个人信息"""
    obj = current.obj
    data = {
        "user_id": current.user_id,
        "username": current.username,
        "role": current.role,
        "avatar": getattr(obj, "avatar", None),
        "phone": getattr(obj, "phone", None),
        "create_time": format_datetime(getattr(obj, "create_time", None)),
    }
    if current.role == "admin":
        data["nickname"] = obj.nickname
        data["email"] = obj.email
    elif current.role == "doctor":
        data["real_name"] = obj.real_name
        data["title"] = obj.title
        data["specialty"] = obj.specialty
        data["introduction"] = obj.introduction
        data["department_id"] = obj.department_id
    elif current.role == "user":
        data["real_name"] = obj.real_name
        data["gender"] = obj.gender
        data["age"] = obj.age
        data["allergy_history"] = obj.allergy_history
    return success(data)


@router.put("/update")
def update_profile(req: ProfileUpdateRequest, db: Session = Depends(get_db), current: CurrentUser = Depends(get_current_user)):
    """更新个人资料"""
    obj = current.obj
    if current.role == "admin":
        if req.nickname is not None: obj.nickname = req.nickname
        if req.phone is not None: obj.phone = req.phone
        if req.email is not None: obj.email = req.email
    elif current.role == "doctor":
        if req.real_name is not None: obj.real_name = req.real_name
        if req.phone is not None: obj.phone = req.phone
        if req.title is not None: obj.title = req.title
        if req.specialty is not None: obj.specialty = req.specialty
        if req.introduction is not None: obj.introduction = req.introduction
    elif current.role == "user":
        if req.real_name is not None: obj.real_name = req.real_name
        if req.phone is not None: obj.phone = req.phone
        if req.gender is not None: obj.gender = req.gender
        if req.age is not None: obj.age = req.age
        if req.allergy_history is not None: obj.allergy_history = req.allergy_history
    db.commit()
    return success(None, "资料更新成功")


@router.put("/password")
def change_password(req: PasswordChangeRequest, db: Session = Depends(get_db), current: CurrentUser = Depends(get_current_user)):
    """修改密码"""
    obj = current.obj
    if not verify_password(req.old_password, obj.password):
        return success(None, "原密码错误")
    obj.password = req.new_password
    db.commit()
    return success(None, "密码修改成功")


@router.post("/avatar")
async def upload_avatar(file: UploadFile = File(...), db: Session = Depends(get_db), current: CurrentUser = Depends(get_current_user)):
    """上传头像"""
    content = await file.read()
    rel_path = save_upload_file(content, file.filename, "avatar")
    current.obj.avatar = rel_path
    db.commit()
    return success({"avatar": rel_path}, "头像上传成功")