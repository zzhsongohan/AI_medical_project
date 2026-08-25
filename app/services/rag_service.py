"""RAG检索增强服务"""
import json
import os
import sys
import time
from typing import AsyncGenerator, List, Dict, Any
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.rag.loader import load_document
from app.rag.splitter import split_text
from app.rag.vector_store import get_vector_store
from app.models.knowledge import KnowledgeFile, KnowledgeChunk
from app.services.graph_service import get_graph_service


def _safe_console_text(text: str) -> str:
    """控制台安全输出（避免GBK编码报错）"""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    return text.encode(encoding, errors="replace").decode(encoding, errors="replace")


def _rag_log(tag: str, message: str) -> None:
    """RAG流程控制台日志"""
    try:
        print(f"[RAG-{tag}] {_safe_console_text(message)}", flush=True)
    except Exception:
        pass


class RagService:
    """
    RAG检索增强生成服务 - 医疗问诊AI核心引擎
    融合向量检索（Chroma）+ 知识图谱推理（Neo4j）+ 大模型生成（DeepSeek）
    提供知识库文件处理、上下文构建、SSE流式对话等能力
    """

    def __init__(self):
        """初始化RAG服务依赖：大模型、向量存储、知识图谱"""
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            openai_api_key=settings.llm_api_key,
            openai_api_base=settings.llm_base_url,
            streaming=True,
            temperature=0.7,
        )
        self.vector_store = get_vector_store()
        self.graph_service = get_graph_service()

    def process_file(self, db: Session, file_record: KnowledgeFile) -> int:
        """
        处理知识库文件全流程：
        1. 标记为处理中（vector_status=1）
        2. 解析文件提取纯文本
        3. 递归字符分块（带重叠）
        4. 清理旧分块和旧向量
        5. 批量写入分块记录 + 向量化存入Chroma
        6. 标记为完成（vector_status=2），失败则标记为3
        """
        # 先标记为处理中，防止重复处理
        file_record.vector_status = 1
        db.commit()
        try:
            #将数据库里存的路径转换为当前系统能读到的绝对路径

            # 统一路径格式，兼容Windows和Linux
            abs_path = file_record.file_path.replace("\\", "/")
            abs_path = abs_path.replace("/", os.sep)
            # 步骤1：加载文档内容（支持txt/pdf/doc/md等格式）
            text = load_document(abs_path)
            # 步骤2：文本分块（按chunk_size=500，重叠80字符）
            chunks = split_text(text)

            # 步骤3：清理该文件的旧分块和旧向量（幂等处理）
            db.query(KnowledgeChunk).filter(KnowledgeChunk.file_id == file_record.id).delete()
            self.vector_store.delete_by_file_id(file_record.id)

            # 步骤4：批量构建分块记录和向量数据
            texts, metadatas, ids = [], [], []
            for idx, chunk in enumerate(chunks):
                vector_id = f"file_{file_record.id}_chunk_{idx}"
                db_chunk = KnowledgeChunk(
                    file_id=file_record.id,
                    chunk_index=idx,
                    content=chunk,
                    vector_id=vector_id,
                )
                db.add(db_chunk)
                texts.append(chunk)
                metadatas.append({"file_id": file_record.id, "file_name": file_record.file_name, "chunk_index": idx})
                ids.append(vector_id)
            db.commit()
            # 步骤5：批量向量化并写入Chroma（分批调用嵌入API，避免超限）
            if texts:
                self.vector_store.add_documents(texts, metadatas, ids)
            # 标记处理完成
            file_record.chunk_count = len(chunks)
            file_record.vector_status = 2
            db.commit()
            return len(chunks)
        except Exception as e:
            # 异常时标记为失败状态
            file_record.vector_status = 3
            db.commit()
            raise e

    def _extract_symptoms(self, query: str) -> List[str]:
        """
        从用户查询中提取症状关键词（基于关键词匹配的简易NER）
        用于触发知识图谱推理，补充向量检索之外的结构化医疗知识
        """
        common_symptoms = [
            "头痛", "发热", "咳嗽", "乏力", "恶心", "呕吐", "腹泻", "腹痛",
            "胸闷", "心悸", "头晕", "失眠", "皮疹", "瘙痒", "水肿", "出血",
            "关节痛", "腰痛", "视力模糊", "耳鸣", "鼻塞", "咽痛", "流涕",
            "高血压", "糖尿病", "感冒", "发烧", "过敏", "便秘", "尿频",
        ]
        return [s for s in common_symptoms if s in query]

    def _build_context(self, query: str) -> tuple[str, List[Dict], List[Dict]]:
        """
        构建RAG上下文（混合检索策略）：
        1. 向量检索：从Chroma中检索TopK最相似的文档片段
        2. 图谱增强：提取症状关键词，从Neo4j推理可能疾病
        3. 上下文拼接：将向量结果和图谱结果组装为LLM可理解的prompt上下文
        返回：(上下文文本, 引用文档列表, 图谱推理结果列表)
        """
        _rag_log("检索", f"开始构建上下文，用户问题: {query}")

        # 阶段1：向量相似度检索（语义匹配）
        vector_start = time.time()
        vector_results = self.vector_store.search(query)
        vector_cost = int((time.time() - vector_start) * 1000)
        _rag_log("检索", f"向量检索完成，耗时 {vector_cost}ms，命中 {len(vector_results)} 条")

        references = []
        context_parts = []
        for i, item in enumerate(vector_results):
            meta = item.get("metadata", {})
            file_name = meta.get("file_name", "未知")
            ref = {"index": i + 1, "file_name": file_name, "content": item["content"][:200]}
            references.append(ref)
            context_parts.append(f"[文档{i+1}] {item['content']}")

        # 阶段2：知识图谱推理（结构化医疗知识补充）
        symptoms = self._extract_symptoms(query)
        graph_results = []
        if symptoms:
            _rag_log("图谱", f"提取症状关键词: {symptoms}")
            graph_start = time.time()
            diseases = self.graph_service.infer_diseases_by_symptoms(symptoms)
            graph_results = diseases
            _rag_log("图谱", f"知识图谱检索完成，命中 {len(diseases)} 条")
            if diseases:
                graph_text = "知识图谱推理结果：\n"
                for d in diseases[:5]:
                    graph_text += f"- 可能疾病: {d.get('disease')} (匹配症状数:{d.get('match_count')}), 建议科室: {d.get('department', '未知')}\n"
                context_parts.append(graph_text)

        # 阶段3：拼接最终上下文文本
        context = "\n\n".join(context_parts) if context_parts else "暂无相关知识库内容。"
        _rag_log("检索", f"上下文构建完成，参考内容长度 {len(context)} 字符")
        return context, references, graph_results

    async def chat_stream(self, query: str, history: List[Dict] = None) -> AsyncGenerator[str, None]:
        """
        SSE流式对话接口 - AI问诊核心方法
        流程：构建上下文 -> 组装消息（系统提示+历史对话+用户问题）
             -> 调用LLM流式生成 -> 逐块推送SSE事件 -> 结束时推送引用和耗时
        """
        start_time = time.time()
        history = history or []
        _rag_log("LLM", f"收到问诊请求，历史消息 {len(history)} 条")
        # 步骤1：构建RAG增强上下文
        context, references, graph_results = self._build_context(query)

        # 步骤2：系统提示词 - 设定AI助手角色和医疗免责声明
        system_prompt = """你是AI智能医疗问诊助手，基于提供的知识库和医疗知识图谱为用户提供健康咨询。
请注意：
1. 你的回答仅供参考，不能替代专业医生的诊断
2. 如有严重症状，请建议用户及时就医
3. 结合知识库内容和图谱推理结果给出专业、易懂的建议
4. 回答要条理清晰，适当分点说明"""

        # 步骤3：用户消息 - 注入检索到的上下文
        user_prompt = f"""参考知识：
{context}

用户问题：{query}

请基于以上参考信息回答用户问题。"""

        # 步骤4：组装消息列表（保留最近6轮历史对话）
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            for h in history[-6:]:
                messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": user_prompt})

        # 步骤5：调用大模型流式生成，逐块推送SSE事件
        llm_start = time.time()
        full_content = ""
        chunk_count = 0
        try:
            async for chunk in self.llm.astream(messages):
                if chunk.content:
                    full_content += chunk.content
                    chunk_count += 1
                    # SSE格式：data: {json}\n\n  类型为content表示正文片段
                    yield f"data: {json.dumps({'type': 'content', 'content': chunk.content}, ensure_ascii=False)}\n\n"
        except Exception as e:
            llm_cost = int((time.time() - llm_start) * 1000)
            _rag_log("LLM", f"大模型请求失败，耗时 {llm_cost}ms，错误: {e}")
            raise

        # 步骤6：流式结束，推送done事件（附带引用来源、图谱结果、耗时统计）
        llm_cost = int((time.time() - llm_start) * 1000)
        total_cost = int((time.time() - start_time) * 1000)
        _rag_log("LLM", f"大模型回复完成，流式块数={chunk_count}，回复长度={len(full_content)} 字符，LLM耗时={llm_cost}ms，总耗时={total_cost}ms")

        cost_time = int((time.time() - start_time) * 1000)
        yield f"data: {json.dumps({'type': 'done', 'references': references, 'graph': graph_results, 'cost_time': cost_time}, ensure_ascii=False)}\n\n"


_rag_service = None


def get_rag_service() -> RagService:
    """获取RAG服务单例"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RagService()
    return _rag_service