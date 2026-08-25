# 加载 .env 文件（从项目根目录找）
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent  # app/ 目录
PROJECT_ROOT = BASE_DIR.parent  # 项目根目录（docker-compose.yml 所在目录）
load_dotenv(PROJECT_ROOT / ".env")

# 项目名称
PROJECT_NAME = "AI智能医疗问诊平台系统"

# MySQL数据库配置（从环境变量读取）
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3309"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "zzh2864799")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "db_ai_medical")
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

# Neo4j知识图谱配置
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "12345678")



# LLM大模型配置（阿里百炼兼容模式）
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
DASHSCOPE_BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://deepseek-ai.com/v1")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")
EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", "2048"))
EMBEDDING_BATCH_SIZE = 10

# 文件上传目录
UPLOAD_DIR = os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads"))

# Chroma向量数据库目录
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(BASE_DIR / "chroma_db"))
CHROMA_COLLECTION = "medical_knowledge"

# JWT配置
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ai-medical-consult-secret-key-2026")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))

# RAG配置
CHUNK_SIZE = 500
CHUNK_OVERLAP = 80
RETRIEVAL_TOP_K = 5

# 启动时检查API Key
if not DASHSCOPE_API_KEY:
    print("[警告] 未检测到环境变量 DASHSCOPE_API_KEY，LLM和向量化功能将无法正常使用！")


class Settings:
    """配置类 - 统一访问入口"""
    project_name: str = PROJECT_NAME
    base_dir: Path = BASE_DIR
    database_url: str = DATABASE_URL
    neo4j_uri: str = NEO4J_URI
    neo4j_user: str = NEO4J_USER
    neo4j_password: str = NEO4J_PASSWORD
    dashscope_api_key: str = DASHSCOPE_API_KEY
    dashscope_base_url: str = DASHSCOPE_BASE_URL

    llm_model: str = LLM_MODEL
    llm_api_key: str = DEEPSEEK_API_KEY
    llm_base_url: str = DEEPSEEK_BASE_URL

    embedding_model: str = EMBEDDING_MODEL
    embedding_dimensions: int = EMBEDDING_DIMENSIONS
    embedding_batch_size: int = EMBEDDING_BATCH_SIZE
    upload_dir: str = UPLOAD_DIR
    chroma_persist_dir: str = CHROMA_PERSIST_DIR
    chroma_collection: str = CHROMA_COLLECTION
    jwt_secret_key: str = JWT_SECRET_KEY
    jwt_algorithm: str = JWT_ALGORITHM
    jwt_expire_minutes: int = JWT_EXPIRE_MINUTES
    chunk_size: int = CHUNK_SIZE
    chunk_overlap: int = CHUNK_OVERLAP
    retrieval_top_k: int = RETRIEVAL_TOP_K


settings = Settings()