from typing import List, Dict, Any, Optional

from neo4j import GraphDatabase
from app.core.config import settings

class GraphService:
    """知识图谱业务逻辑"""
    # 症状别名映射表：将用户口语化表述统一映射为标准症状名称，提升召回率
    SYMPTOM_ALIASES = {
        "头疼": "头痛",
        "头胀": "头痛",
        "头昏": "头晕",
        "发烧": "发热",
        "发高烧": "发热",
        "高烧": "发热",
        "低烧": "发热",
        "肚子痛": "腹痛",
        "胃疼": "腹痛",
        "胸口痛": "胸痛",
        "胸口闷": "胸闷",
        "没力气": "乏力", "疲倦": "乏力", "疲劳": "乏力",
        "想吐": "恶心",
        "拉肚子": "腹泻",
        "关节疼": "关节痛",
        "腰疼": "腰痛",
        "看不清": "视力模糊",
        "流鼻涕": "流涕",
        "喉咙痛": "咽痛", "嗓子痛": "咽痛",
    }


    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )

    def close(self):
        self.driver.close()

    def _normalize_symptoms(self, symptoms: List[str]) -> List[str]:
        """
        症状别名归一化：
        - 去除空白和空值
        - 通过别名表将口语化症状名转为标准名
        - 去重并保持原有顺序
        """
        normalized: List[str] = []
        for symptom in symptoms:
            name = (symptom or "").strip()
            if not name:
                continue
            # 别名映射：找不到则保留原名
            normalized.append(self.SYMPTOM_ALIASES.get(name, name))
        # 利用dict.fromkeys去重并保持顺序
        return list(dict.fromkeys(normalized))


    def infer_diseases_by_symptoms(self, symptoms: List[str]) -> List[Dict]:
        """
        根据症状推理可能疾病（基于共现症状数排序的协同过滤思路）：
        1. 先做症状归一化
        2. Cypher查询：匹配所有包含任一输入症状的疾病
        3. 按匹配症状数量降序排列（匹配越多越可能）
        4. 计算概率 = 匹配症状数 / 输入症状总数
        5. 返回Top10可能疾病及建议科室
        """
        normalized_symptoms = self._normalize_symptoms(symptoms)
        if not normalized_symptoms:
            return []
        # Cypher查询：UNWIND展开症状列表 -> 匹配疾病-症状关系 -> 聚合统计匹配数
        query = """
        UNWIND $symptoms AS symptom_name
        MATCH (s:Symptom {name: symptom_name})<-[:HAS_SYMPTOM]-(d:Disease)
        OPTIONAL MATCH (d)-[:BELONGS_TO]->(dep:Department)
        WITH d, dep, count(s) AS match_count, collect(symptom_name) AS matched
        ORDER BY match_count DESC
        LIMIT 10
        RETURN d.name AS disease, match_count, dep.name AS department, matched
        """
        total = len(normalized_symptoms)
        with self.driver.session() as session:
            result = session.run(query, symptoms=normalized_symptoms)
            rows = [dict(r) for r in result]
        # 组装返回结构，包含疾病名、匹配数、概率、科室、匹配的症状列表
        return [
            {
                "name": row["disease"],
                "disease": row["disease"],
                "match_count": row["match_count"],
                "probability": round(row["match_count"] / total, 2),
                "department": row.get("department") or "-",
                "matched": row.get("matched") or [],
            }
            for row in rows
        ]

    def get_disease_detail(self, disease_name: str) -> Dict[str, Any]:
        """
        获取疾病详情子图：
        一次性查询疾病关联的所有维度：症状、科室、推荐药物、检查项目、
        并发症、宜吃食物、忌吃食物，组装为结构化详情返回
        """
        query = """
        MATCH (d:Disease {name: $name})
        OPTIONAL MATCH (d)-[:HAS_SYMPTOM]->(s:Symptom)
        OPTIONAL MATCH (d)-[:BELONGS_TO]->(dep:Department)
        OPTIONAL MATCH (d)-[:RECOMMEND_DRUG]->(drug:Drug)
        OPTIONAL MATCH (d)-[:NEED_CHECK]->(chk:Check)
        OPTIONAL MATCH (d)-[:ACCOMPANY_WITH]->(comp:Disease)
        OPTIONAL MATCH (d)-[:SHOULD_EAT]->(food:Food)
        OPTIONAL MATCH (d)-[:AVOID_EAT]->(avoid:Food)
        RETURN d.name AS disease,
               collect(DISTINCT s.name) AS symptoms,
               dep.name AS department,
               collect(DISTINCT drug.name) AS drugs,
               collect(DISTINCT chk.name) AS checks,
               collect(DISTINCT comp.name) AS complications,
               collect(DISTINCT food.name) AS should_eat,
               collect(DISTINCT avoid.name) AS avoid_eat
        """
        with self.driver.session() as session:
            record = session.run(query, name=disease_name).single()
            if not record:
                return {}
            detail = dict(record)
            drugs = detail.get("drugs") or []
            checks = detail.get("checks") or []
            detail["name"] = detail.get("disease") or disease_name
            # 补充描述性字段，方便前端直接展示
            detail["description"] = f"建议检查：{'、'.join(checks)}" if checks else "-"
            detail["treatment"] = f"常用药物：{'、'.join(drugs)}" if drugs else "-"
            return detail

    def get_entity_subgraph(self, entity_name: str, depth: int = 1) -> Dict[str, Any]:
        """获取实体邻居子图（供前端可视化）"""
        nodes_map = {}
        links = []
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n {name: $name})-[r]-(m) RETURN n, type(r) AS rel, m LIMIT 30",
                name=entity_name,
            )
            for record in result:
                n = record["n"]
                m = record["m"]
                rel = record["rel"]
                n_id = n.element_id
                m_id = m.element_id
                n_label = list(n.labels)[0] if n.labels else "Unknown"
                m_label = list(m.labels)[0] if m.labels else "Unknown"
                nodes_map[n_id] = {"id": n_id, "name": n.get("name", ""), "category": n_label, "group": n_label}
                nodes_map[m_id] = {"id": m_id, "name": m.get("name", ""), "category": m_label, "group": m_label}
                links.append({"source": n_id, "target": m_id, "relation": rel})
        return {"nodes": list(nodes_map.values()), "links": links}

    def search_entities(self, keyword: str) -> List[Dict]:
        """搜索图谱实体（支持症状别名归一化）"""
        keyword = (keyword or "").strip()
        if not keyword:
            return []
        # 别名归一化：如果关键词在别名表中，同时搜索映射后的标准名
        search_terms = {keyword}
        if keyword in self.SYMPTOM_ALIASES:
            search_terms.add(self.SYMPTOM_ALIASES[keyword])
        # 反过来：如果关键词本身就是标准名，也搜索其别名（扩充召回）
        for alias, standard in self.SYMPTOM_ALIASES.items():
            if standard == keyword:
                search_terms.add(alias)
        # 用 OR 条件一次查询
        query = """
        MATCH (n) WHERE any(term IN $terms WHERE n.name CONTAINS term)
        RETURN n.name AS name, labels(n)[0] AS label
        LIMIT 20
        """
        with self.driver.session() as session:
            result = session.run(query, terms=list(search_terms))
            return [dict(r) for r in result]

    def get_full_graph(self) -> Dict[str, Any]:
        """获取完整知识图谱"""
        nodes_map: Dict[str, Dict] = {}
        links: List[Dict] = []
        query = "MATCH (a)-[r]->(b) RETURN a, type(r) AS rel, b"
        with self.driver.session() as session:
            result = session.run(query)
            for record in result:
                a = record["a"]
                b = record["b"]
                rel = record["rel"]
                a_id = a.element_id
                b_id = b.element_id
                a_label = list(a.labels)[0] if a.labels else "Unknown"
                b_label = list(b.labels)[0] if b.labels else "Unknown"
                nodes_map[a_id] = {"id": a_id, "name": a.get("name", ""), "category": a_label, "group": a_label}
                nodes_map[b_id] = {"id": b_id, "name": b.get("name", ""), "category": b_label, "group": b_label}
                links.append({"source": a_id, "target": b_id, "relation": rel})
        return {"nodes": list(nodes_map.values()), "links": links}


    def get_graph_stats(self) -> Dict[str, int]:
        """获取图谱统计"""
        query = """
        MATCH (n) WITH labels(n)[0] AS label, count(n) AS cnt
        RETURN label, cnt ORDER BY cnt DESC
        """
        with self.driver.session() as session:
            result = session.run(query)
            return {r["label"]: r["cnt"] for r in result}



_graph_service:Optional[GraphService] = None


def get_graph_service():
    """单例获取图谱服务"""
    global _graph_service
    if _graph_service is None:
        _graph_service = GraphService()
    return _graph_service