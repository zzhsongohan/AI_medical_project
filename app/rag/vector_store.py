"""Chroma向量数据库封装"""
import os
from typing import List, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core.config import settings
from app.rag.embeddings import get_embeddings


class VectorStore:
    """
    Chroma向量存储管理器
    - 持久化存储到本地磁盘
    - 使用余弦相似度进行向量检索
    - 支持批量添加、相似度检索、按文件删除
    """

    def __init__(self):
        """初始化Chroma客户端：创建持久化目录、获取/创建集合、加载嵌入模型"""
        os.makedirs(settings.chroma_persist_dir, exist_ok=True)
        # 持久化客户端：数据存储在本地磁盘，重启不丢失
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        # 获取或创建集合，使用余弦相似度作为距离度量（hnsw:space=cosine）
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection,
            metadata={"hnsw:space": "cosine"},
        )
        # 加载嵌入模型（阿里云text-embedding-v4）
        self.embeddings = get_embeddings()

    def add_documents(self, texts: List[str], metadatas: List[dict], ids: List[str]):
        """
        添加文档向量（分批嵌入）
        分批调用嵌入API，避免单次请求过大触发API限流
        """
        batch_size = settings.embedding_batch_size
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_metas = metadatas[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            # 调用嵌入模型生成向量
            vectors = self.embeddings.embed_documents(batch_texts)
            self.collection.add(
                documents=batch_texts,
                embeddings=vectors,
                metadatas=batch_metas,
                ids=batch_ids,
            )

    def search(self, query: str, top_k: int = None) -> List[dict]:
        """
        向量相似度检索
        将查询文本转为向量，在Chroma中检索最相似的TopK个文档片段
        返回内容、元数据、距离（余弦距离，越小越相似）
        """
        top_k = top_k or settings.retrieval_top_k
        query_vector = self.embeddings.embed_query(query)
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        items = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                items.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0,
                })
        return items

    def delete_by_file_id(self, file_id: int):
        """删除指定文件的所有向量（按metadata中的file_id过滤）"""
        try:
            self.collection.delete(where={"file_id": file_id})
        except Exception:
            pass


_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """获取向量存储单例"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store