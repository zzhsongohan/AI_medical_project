"""文档加载器 - 支持txt/doc/pdf/markdown"""
import os
from pathlib import Path


def load_document(file_path: str) -> str:
    """加载并解析文档内容"""
    ext = Path(file_path).suffix.lower()
    if ext in (".txt", ".md", ".markdown"):
        return _load_text(file_path)
    elif ext == ".pdf":
        return _load_pdf(file_path)
    elif ext in (".doc", ".docx"):
        return _load_docx(file_path)
    else:
        raise ValueError(f"不支持的文件类型: {ext}")


def _load_text(file_path: str) -> str:
    """加载纯文本/markdown文件"""
    for encoding in ("utf-8", "gbk", "gb2312", "latin-1"):
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"无法解码文件: {file_path}")


def _load_pdf(file_path: str) -> str:
    """加载PDF文件"""
    from pypdf import PdfReader
    reader = PdfReader(file_path)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n".join(pages)


def _load_docx(file_path: str) -> str:
    """加载Word文档"""
    ext = Path(file_path).suffix.lower()
    if ext == ".docx":
        from docx import Document
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    else:
        with open(file_path, "rb") as f:
            raw = f.read()
        try:
            text = raw.decode("utf-8", errors="ignore")
            return "".join(c for c in text if c.isprintable() or c in "\n\r\t")
        except Exception:
            raise ValueError(f"无法解析.doc文件: {file_path}")