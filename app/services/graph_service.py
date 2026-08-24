from neo4j import GraphDatabase
from app.core.config import settings

class GraphService:
    """知识图谱业务逻辑"""

    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )

    def close(self):
        self.driver.close()

    def infer_diseases_by_symptoms(self, symptom_list):
        """根据症状列表推理可能的疾病（症状共现统计）"""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (d:Disease)-[:HAS_SYMPTOM]->(s:Symptom) "
                "WHERE s.name IN $symptoms "
                "WITH d, count(s) AS match_count, collect(s.name) AS matched_symptoms "
                "ORDER BY match_count DESC "
                "LIMIT 10 "
                "OPTIONAL MATCH (d)-[:BELONGS_TO]->(dep:Department) "
                "RETURN d.name AS disease, match_count, matched_symptoms, dep.name AS department",
                symptoms=symptom_list
            )
            return [
                {
                    "disease": record["disease"],
                    "match_count": record["match_count"],
                    "matched_symptoms": record["matched_symptoms"],
                    "department": record["department"],
                }
                for record in result
            ]

    def get_disease_detail(self, disease_name):
        """获取疾病详情：症状、推荐药品、所属科室"""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (d:Disease {name: $name}) "
                "OPTIONAL MATCH (d)-[:HAS_SYMPTOM]->(s:Symptom) "
                "OPTIONAL MATCH (d)-[:RECOMMEND_DRUG]->(dr:Drug) "
                "OPTIONAL MATCH (d)-[:BELONGS_TO]->(dep:Department) "
                "RETURN d.name AS disease, "
                "collect(DISTINCT s.name) AS symptoms, "
                "collect(DISTINCT dr.name) AS drugs, "
                "dep.name AS department",
                name=disease_name
            )
            record = result.single()
            if not record:
                return None
            return {
                "disease": record["disease"],
                "symptoms": record["symptoms"],
                "drugs": record["drugs"],
                "department": record["department"],
            }

    def get_graph_data(self, limit=100):
        """获取图谱数据用于前端可视化"""
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n)-[r]->(m) "
                "RETURN n, r, m "
                "LIMIT $limit",
                limit=limit
            )
            nodes = {}
            edges = []
            for record in result:
                n = record["n"]
                m = record["m"]
                r = record["r"]
                for node in [n, m]:
                    nid = str(node.element_id)
                    if nid not in nodes:
                        nodes[nid] = {
                            "id": nid,
                            "name": node["name"],
                            "category": list(node.labels)[0],
                        }
                edges.append({
                    "source": str(n.element_id),
                    "target": str(m.element_id),
                    "relation": type(r).__name__,
                })
            return {"nodes": list(nodes.values()), "edges": edges}


    def get_all_symptoms(self):
        """获取所有症状列表（用于症状选择）"""
        with self.driver.session() as session:
            result = session.run("MATCH (s:Symptom) RETURN s.name AS name ORDER BY s.name")
            return [record["name"] for record in result]

_graph_service = None


def get_graph_service():
    """单例获取图谱服务"""
    global _graph_service
    if _graph_service is None:
        _graph_service = GraphService()
    return _graph_service