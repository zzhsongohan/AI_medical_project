"""嵌入模型封装 - text-embedding-v4（兼容阿里云百炼）"""
from typing import List
from openai import OpenAI
from langchain_core.embeddings import Embeddings
from app.core.config import settings


class AlibabaEmbeddings(Embeddings):
    """
    阿里云百炼嵌入模型封装，兼容LangChain的Embeddings接口
    通过OpenAI SDK调用阿里云百炼的text-embedding-v4模型
    支持批量文档嵌入和单条查询嵌入
    """

    def __init__(self):
        """初始化 DashScope 嵌入服务（OpenAI 兼容协议）"""
        self.client = OpenAI(
            api_key=settings.dashscope_api_key,
            base_url=settings.dashscope_base_url,
        )
        self.model = settings.embedding_model
        self.dimensions = settings.embedding_dimensions
        self.batch_size = settings.embedding_batch_size

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        批量嵌入文档
        - 空文本用空格占位（避免API报错）
        - 按batch_size分批调用，防止单次请求超限
        """
        all_embeddings = []
        # 空文本兜底：嵌入API不接受空字符串，用空格代替
        valid_texts = [t if t and t.strip() else " " for t in texts]
        for i in range(0, len(valid_texts), self.batch_size):
            batch = valid_texts[i:i + self.batch_size]
            response = self.client.embeddings.create(
                model=self.model,
                input=batch,
                dimensions=self.dimensions,
            )
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
        return all_embeddings

    def embed_query(self, text: str) -> List[float]:
        """嵌入单条查询文本（用于向量检索时的查询向量化）"""
        response = self.client.embeddings.create(
            model=self.model,
            input=text if text and text.strip() else " ",
            dimensions=self.dimensions,
        )
        return response.data[0].embedding


def get_embeddings() -> Embeddings:
    """获取嵌入模型实例"""
    return AlibabaEmbeddings()