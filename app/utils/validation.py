"""参数校验错误格式化工具"""
def format_validation_errors(errors: list) -> str:
    """将FastAPI参数校验错误转为中文提示"""
    messages = []
    for err in errors:
        field = ".".join(str(loc) for loc in err.get("loc", []) if loc != "body")
        msg = err.get("msg", "参数错误")
        if field:
            messages.append(f"{field}: {msg}")
        else:
            messages.append(msg)
    return "；".join(messages)


