"""文本分块器"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings


def split_text(text: str) -> list[str]:
    """将文本分割为多个块"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", "；", " ", ""],
    )
    return splitter.split_text(text)

