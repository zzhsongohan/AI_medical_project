"""请求参数校验错误中文提示"""
FIELD_LABELS = {
    "username": "用户名", "password": "密码", "confirm_password": "确认密码",
    "old_password": "原密码", "new_password": "新密码", "real_name": "用户昵称",
    "phone": "手机号", "email": "邮箱", "gender": "性别", "age": "年龄",
    "allergy_history": "过敏史", "status": "状态", "title": "标题",
    "content": "内容", "name": "名称", "message": "消息内容", "chief_complaint": "主诉",
}

def _field_label(field: str) -> str:
    return FIELD_LABELS.get(field, field)

def translate_validation_error(err: dict) -> str:
    loc = err.get("loc") or []
    field_key = ""
    for item in reversed(loc):
        if isinstance(item, str) and item not in ("body", "query", "path"):
            field_key = item
            break
    label = _field_label(field_key) if field_key else "请求参数"
    err_type = err.get("type", "")
    ctx = err.get("ctx") or {}
    msg = str(err.get("msg") or "")
    if err_type == "string_too_short":
        return f"{label}至少{ctx.get('min_length', 0)}个字符"
    if err_type == "string_too_long":
        return f"{label}不能超过{ctx.get('max_length', 0)}个字符"
    if err_type == "missing":
        return f"请填写{label}"
    if err_type == "int_parsing":
        return f"{label}必须为整数"
    return msg or "请求参数不正确"

def format_validation_errors(errors: list) -> str:
    if not errors:
        return "请求参数不正确"
    messages = []
    for err in errors:
        text = translate_validation_error(err)
        if text and text not in messages:
            messages.append(text)
    return "；".join(messages)