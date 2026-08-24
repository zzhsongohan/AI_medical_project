from fastapi import APIRouter
from pydantic import BaseModel

from app.core.response import success
from app.services.graph_service import get_graph_service

router = APIRouter()

class SymptomCheckRequest(BaseModel):
    symptoms: list[str]



@router.get("/symptoms")
def get_symptoms():
    """获取所有症状列表"""
    data = get_graph_service().get_all_symptoms()
    return success(data)


@router.post("/symptom-check")
def symptom_check(req: SymptomCheckRequest):
    """症状自查 - 根据输入的症状推理可能疾病"""
    result = get_graph_service().infer_diseases_by_symptoms(req.symptoms)
    return success(result)


@router.get("/disease/{name}")
def disease_detail(name: str):
    """获取疾病详情"""
    data = get_graph_service().get_disease_detail(name)
    return success(data)


@router.get("/visualize")
def visualize(limit: int = 100):
    """知识图谱可视化数据"""
    data = get_graph_service().get_graph_data(limit)
    return success(data)