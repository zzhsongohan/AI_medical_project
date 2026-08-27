"""AI问诊接口 - SSE流式
提供会话管理（列表/消息）和流式对话能力，对话消息持久化到数据库"""
import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.deps import require_roles, CurrentUser
from app.core.response import success
from app.db.session import get_db
from app.models.consult import ConsultSession, ConsultMessage
from app.schemas.common import ChatRequest
from app.services.rag_service import get_rag_service
from app.utils.helpers import format_datetime

router = APIRouter()


@router.get("/sessions")
def list_sessions(db: Session = Depends(get_db), current: CurrentUser = Depends(require_roles("user"))):
    """获取当前用户的问诊会话列表（按更新时间倒序）"""
    items = db.query(ConsultSession).filter(ConsultSession.user_id == current.user_id).order_by(ConsultSession.update_time.desc()).all()
    data = [{"id": s.id, "title": s.title, "message_count": s.message_count, "create_time": format_datetime(s.create_time)} for s in items]
    return success(data)


@router.get("/sessions/{session_id}/messages")
def get_messages(session_id: int, db: Session = Depends(get_db), current: CurrentUser = Depends(require_roles("user"))):
    """获取指定会话的所有消息（按时间正序）"""
    msgs = db.query(ConsultMessage).filter(ConsultMessage.session_id == session_id).order_by(ConsultMessage.id).all()
    data = [{
        "id": m.id, "role": m.role, "content": m.content,
        "references_json": m.references_json, "graph_json": m.graph_json,
        "create_time": format_datetime(m.create_time),
    } for m in msgs]
    return success(data)


@router.post("/send")
async def chat_send(req: ChatRequest, db: Session = Depends(get_db), current: CurrentUser = Depends(require_roles("user"))):
    """
    AI问诊 - SSE流式回复
    流程：
    1. 获取或创建会话（新会话标题取消息前20字）
    2. 保存用户消息到数据库
    3. 加载历史消息（供LLM上下文使用）
    4. 返回SSE流式响应，内部调用RAG服务生成回复
    5. 流式结束后保存AI回复、引用来源、图谱结果
    """
    # 步骤1：获取或创建会话
    if req.session_id:
        session = db.query(ConsultSession).filter(ConsultSession.id == req.session_id, ConsultSession.user_id == current.user_id).first()
    else:
        session = None
    if not session:
        # 新会话：标题截取消息前20字
        title = req.message[:20] + ("..." if len(req.message) > 20 else "")
        session = ConsultSession(user_id=current.user_id, title=title)
        db.add(session)
        db.commit()
        db.refresh(session)

    # 步骤2：保存用户消息
    user_msg = ConsultMessage(session_id=session.id, role="user", content=req.message)
    db.add(user_msg)
    db.commit()

    # 步骤3：加载历史消息（排除刚保存的用户消息，避免重复）
    history_msgs = db.query(ConsultMessage).filter(ConsultMessage.session_id == session.id).order_by(ConsultMessage.id).all()
    history = [{"role": m.role, "content": m.content} for m in history_msgs[:-1]]

    session_id = session.id

    async def event_generator():
        """SSE事件生成器：先推送会话ID，再流式推送AI回复，最后保存AI消息"""
        yield f"data: {json.dumps({'type': 'session', 'session_id': session_id}, ensure_ascii=False)}\n\n"
        full_content = ""
        references = []
        graph_results = []
        cost_time = 0
        try:
            # 调用RAG服务的流式对话，逐块转发SSE事件
            async for chunk in get_rag_service().chat_stream(req.message, history):
                yield chunk
                # 同时解析事件，收集完整回复内容和引用数据（用于持久化）
                if chunk.startswith("data: "):
                    try:
                        data = json.loads(chunk[6:].strip())
                        if data.get("type") == "content":
                            full_content += data["content"]
                        elif data.get("type") == "done":
                            references = data.get("references", [])
                            graph_results = data.get("graph", [])
                            cost_time = data.get("cost_time", 0)
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"
            return

        # 流式结束后，在新的数据库会话中保存AI回复消息（异步生成器中不能复用原请求会话）
        from app.db.session import SessionLocal
        sdb = SessionLocal()
        try:
            # 保存助手消息，附带引用来源和图谱推理结果
            assistant_msg = ConsultMessage(
                session_id=session_id,
                role="assistant",
                content=full_content,
                references_json=json.dumps(references, ensure_ascii=False),
                graph_json=json.dumps(graph_results, ensure_ascii=False),
                cost_time=cost_time,
            )
            sdb.add(assistant_msg)
            # 更新会话消息计数（+2：一条用户消息 + 一条AI回复）
            sess = sdb.query(ConsultSession).filter(ConsultSession.id == session_id).first()
            if sess:
                sess.message_count = (sess.message_count or 0) + 2
            sdb.commit()
        finally:
            sdb.close()

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/admin/sessions")
def admin_sessions(
    page: int = 1, page_size: int = 10,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
):
    """管理员查看所有问诊记录"""
    from core.response import page_result
    from models.user import User
    q = db.query(ConsultSession)
    total = q.count()
    items = q.order_by(ConsultSession.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    user_map = {u.id: u.real_name or u.username for u in db.query(User).all()}
    data = [{
        "id": s.id, "user_id": s.user_id, "user_name": user_map.get(s.user_id, ""),
        "title": s.title, "message_count": s.message_count,
        "create_time": format_datetime(s.create_time),
    } for s in items]
    return page_result(data, total, page, page_size)