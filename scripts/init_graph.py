"""Neo4j医疗知识图谱初始化脚本 - 约60种常见疾病"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "12345678")

# 医疗知识数据合集
MEDICAL_DATA = [
    {
        "disease": "感冒", "department": "内科",
        "symptoms": ["发热", "头痛", "流涕", "咽痛", "咳嗽", "乏力"],
        "drugs": ["感冒灵", "板蓝根", "维C银翘片"],
        "checks": ["血常规", "C反应蛋白"],
        "complications": ["支气管炎", "肺炎"],
        "should_eat": ["温开水", "新鲜水果", "清淡粥"],
        "avoid_eat": ["辛辣食物", "油腻食物", "冷饮"],
    },
    {
        "disease": "高血压", "department": "心血管内科",
        "symptoms": ["头痛", "头晕", "心悸", "胸闷", "乏力"],
        "drugs": ["氨氯地平", "缬沙坦", "氢氯噻嗪"],
        "checks": ["血压监测", "心电图", "肾功能"],
        "complications": ["脑卒中", "冠心病", "肾功能不全"],
        "should_eat": ["低盐饮食", "芹菜", "香蕉"],
        "avoid_eat": ["高盐食物", "腌制品", "动物内脏"],
    },
    {
        "disease": "糖尿病", "department": "内分泌科",
        "symptoms": ["多饮", "多尿", "多食", "乏力", "体重下降", "视力模糊"],
        "drugs": ["二甲双胍", "格列美脲", "胰岛素"],
        "checks": ["空腹血糖", "糖化血红蛋白", "尿常规"],
        "complications": ["糖尿病肾病", "糖尿病视网膜病变"],
        "should_eat": ["粗粮", "绿叶蔬菜", "豆制品"],
        "avoid_eat": ["甜食", "精制碳水", "含糖饮料"],
    },
    {
        "disease": "胃炎", "department": "消化内科",
        "symptoms": ["腹痛", "恶心", "呕吐", "腹胀", "反酸"],
        "drugs": ["奥美拉唑", "铝碳酸镁", "莫沙必利"],
        "checks": ["胃镜", "幽门螺杆菌检测"],
        "complications": ["胃溃疡", "胃癌"],
        "should_eat": ["小米粥", "面条", "蒸蛋"],
        "avoid_eat": ["辛辣食物", "酒精", "咖啡"],
    },
    {
        "disease": "肺炎", "department": "呼吸内科",
        "symptoms": ["发热", "咳嗽", "胸痛", "呼吸困难", "乏力"],
        "drugs": ["阿莫西林", "左氧氟沙星", "布洛芬"],
        "checks": ["胸部CT", "血常规", "痰培养"],
        "complications": ["呼吸衰竭", "脓胸"],
        "should_eat": ["高蛋白食物", "新鲜水果", "温开水"],
        "avoid_eat": ["辛辣刺激", "烟酒"],
    },
    {
        "disease": "支气管炎", "department": "呼吸内科",
        "symptoms": ["咳嗽", "咳痰", "发热", "胸闷", "喘息"],
        "drugs": ["氨溴索", "沙丁胺醇", "阿奇霉素"],
        "checks": ["胸部X光", "肺功能"],
        "complications": ["肺炎", "肺气肿"],
        "should_eat": ["梨", "蜂蜜", "萝卜"],
        "avoid_eat": ["冷饮", "辛辣", "烟酒"],
    },
    {
        "disease": "冠心病", "department": "心血管内科",
        "symptoms": ["胸痛", "胸闷", "心悸", "呼吸困难", "乏力"],
        "drugs": ["阿司匹林", "硝酸甘油", "阿托伐他汀"],
        "checks": ["心电图", "冠脉造影", "心脏彩超"],
        "complications": ["心肌梗死", "心力衰竭"],
        "should_eat": ["深海鱼", "坚果", "橄榄油"],
        "avoid_eat": ["高脂食物", "动物内脏", "油炸食品"],
    },
    {
        "disease": "脑卒中", "department": "神经内科",
        "symptoms": ["头痛", "头晕", "肢体麻木", "言语不清", "面瘫"],
        "drugs": ["阿司匹林", "氯吡格雷", "阿托伐他汀"],
        "checks": ["头颅CT", "MRI", "颈动脉超声"],
        "complications": ["偏瘫", "失语"],
        "should_eat": ["低盐低脂饮食", "深海鱼", "蔬菜"],
        "avoid_eat": ["高盐", "高脂", "烟酒"],
    },
    {
        "disease": "偏头痛", "department": "神经内科",
        "symptoms": ["头痛", "恶心", "呕吐", "畏光", "头晕"],
        "drugs": ["布洛芬", "舒马曲坦", "氟桂利嗪"],
        "checks": ["头颅MRI", "经颅多普勒"],
        "complications": ["慢性 daily 头痛"],
        "should_eat": ["镁含量高的食物", "全谷物"],
        "avoid_eat": ["巧克力", "奶酪", "红酒"],
    },
    {
        "disease": "失眠", "department": "神经内科",
        "symptoms": ["失眠", "乏力", "头晕", "焦虑", "记忆力下降"],
        "drugs": ["艾司唑仑", "佐匹克隆", "褪黑素"],
        "checks": ["多导睡眠监测", "心理评估"],
        "complications": ["抑郁症", "焦虑症"],
        "should_eat": ["牛奶", "香蕉", "核桃"],
        "avoid_eat": ["咖啡", "浓茶", "酒精"],
    },
    {
        "disease": "湿疹", "department": "皮肤科",
        "symptoms": ["皮疹", "瘙痒", "红肿", "脱屑"],
        "drugs": ["氢化可的松", "他克莫司", "氯雷他定"],
        "checks": ["过敏原检测", "皮肤镜"],
        "complications": ["皮肤感染"],
        "should_eat": ["清淡饮食", "维生素C"],
        "avoid_eat": ["海鲜", "辛辣", "发物"],
    },
    {
        "disease": "痤疮", "department": "皮肤科",
        "symptoms": ["皮疹", "红肿", "瘙痒", "疼痛"],
        "drugs": ["维A酸", "过氧化苯甲酰", "多西环素"],
        "checks": ["激素水平检测"],
        "complications": ["瘢痕", "色素沉着"],
        "should_eat": ["清淡饮食", "锌含量食物"],
        "avoid_eat": ["高糖食物", "乳制品", "辛辣"],
    },
    {
        "disease": "过敏性鼻炎", "department": "耳鼻喉科",
        "symptoms": ["鼻塞", "流涕", "打喷嚏", "瘙痒", "嗅觉减退"],
        "drugs": ["氯雷他定", "布地奈德鼻喷雾", "孟鲁司特"],
        "checks": ["过敏原检测", "鼻内窥镜"],
        "complications": ["鼻窦炎", "哮喘"],
        "should_eat": ["蜂蜜", "姜", "维生素C"],
        "avoid_eat": ["冷饮", "海鲜"],
    },
    {
        "disease": "中耳炎", "department": "耳鼻喉科",
        "symptoms": ["耳痛", "耳鸣", "听力下降", "发热", "流涕"],
        "drugs": ["阿莫西林", "氧氟沙星滴耳液", "布洛芬"],
        "checks": ["耳镜检查", "听力测试"],
        "complications": ["鼓膜穿孔", "听力永久损伤"],
        "should_eat": ["清淡饮食", "高蛋白"],
        "avoid_eat": ["辛辣", "海鲜"],
    },
    {
        "disease": "结膜炎", "department": "眼科",
        "symptoms": ["眼红", "眼痒", "流泪", "异物感", "视力模糊"],
        "drugs": ["左氧氟沙星滴眼液", "色甘酸钠", "人工泪液"],
        "checks": ["裂隙灯检查"],
        "complications": ["角膜炎"],
        "should_eat": ["胡萝卜", "蓝莓", "绿叶蔬菜"],
        "avoid_eat": ["辛辣", "烟酒"],
    },
    {
        "disease": "白内障", "department": "眼科",
        "symptoms": ["视力模糊", "畏光", "视物重影", "色觉改变"],
        "drugs": ["吡诺克辛滴眼液", "谷胱甘肽"],
        "checks": ["视力检查", "裂隙灯", "眼底检查"],
        "complications": ["青光眼"],
        "should_eat": ["富含抗氧化物食物", "深色蔬菜"],
        "avoid_eat": ["高糖", "高盐"],
    },
    {
        "disease": "骨折", "department": "骨科",
        "symptoms": ["疼痛", "肿胀", "活动受限", "畸形"],
        "drugs": ["布洛芬", "钙片", "骨肽"],
        "checks": ["X光", "CT", "MRI"],
        "complications": ["骨不连", "感染"],
        "should_eat": ["高钙食物", "蛋白质", "维生素D"],
        "avoid_eat": ["烟酒", "碳酸饮料"],
    },
    {
        "disease": "腰椎间盘突出", "department": "骨科",
        "symptoms": ["腰痛", "下肢麻木", "疼痛", "活动受限"],
        "drugs": ["甲钴胺", "塞来昔布", "甘露醇"],
        "checks": ["腰椎MRI", "X光"],
        "complications": ["马尾综合征"],
        "should_eat": ["高钙", "维生素D", "蛋白质"],
        "avoid_eat": ["久坐", "重物搬运"],
    },
    {
        "disease": "关节炎", "department": "骨科",
        "symptoms": ["关节痛", "肿胀", "活动受限", "晨僵"],
        "drugs": ["塞来昔布", "氨基葡萄糖", "甲氨蝶呤"],
        "checks": ["X光", "类风湿因子", "血沉"],
        "complications": ["关节畸形", "功能障碍"],
        "should_eat": ["深海鱼", "姜黄", "橄榄油"],
        "avoid_eat": ["高嘌呤", "红肉", "酒精"],
    },
    {
        "disease": "尿路感染", "department": "泌尿外科",
        "symptoms": ["尿频", "尿急", "尿痛", "发热", "腹痛"],
        "drugs": ["左氧氟沙星", "磷霉素", "三金片"],
        "checks": ["尿常规", "尿培养", "泌尿系B超"],
        "complications": ["肾盂肾炎", "败血症"],
        "should_eat": ["大量饮水", " cranberry juice"],
        "avoid_eat": ["辛辣", "酒精"],
    },
    {
        "disease": "肾结石", "department": "泌尿外科",
        "symptoms": ["腰痛", "血尿", "尿频", "恶心", "呕吐"],
        "drugs": ["坦索罗辛", "双氯芬酸钠", "碳酸氢钠"],
        "checks": ["泌尿系B超", "CT", "尿常规"],
        "complications": ["肾积水", "肾功能损害"],
        "should_eat": ["大量饮水", "低草酸饮食"],
        "avoid_eat": ["高草酸食物", "动物蛋白过量"],
    },
    {
        "disease": "贫血", "department": "血液科",
        "symptoms": ["乏力", "头晕", "心悸", "面色苍白", "气短"],
        "drugs": ["硫酸亚铁", "叶酸", "维生素B12"],
        "checks": ["血常规", "铁代谢", "骨髓穿刺"],
        "complications": ["心力衰竭"],
        "should_eat": ["红肉", "动物肝脏", "菠菜"],
        "avoid_eat": ["茶", "咖啡（影响铁吸收）"],
    },
    {
        "disease": "甲状腺功能亢进", "department": "内分泌科",
        "symptoms": ["心悸", "多汗", "体重下降", "手抖", "易怒", "失眠"],
        "drugs": ["甲巯咪唑", "普萘洛尔", "左甲状腺素"],
        "checks": ["甲状腺功能", "甲状腺B超", "TRAb"],
        "complications": ["甲亢危象", "心房颤动"],
        "should_eat": ["高热量高蛋白", "含钙食物"],
        "avoid_eat": ["碘盐", "海带", "紫菜"],
    },
    {
        "disease": "甲状腺功能减退", "department": "内分泌科",
        "symptoms": ["乏力", "怕冷", "体重增加", "便秘", "记忆力下降"],
        "drugs": ["左甲状腺素"],
        "checks": ["甲状腺功能", "TPOAb", "甲状腺B超"],
        "complications": ["黏液性水肿昏迷"],
        "should_eat": ["均衡饮食", "含碘适量"],
        "avoid_eat": ["大量生食十字花科蔬菜"],
    },
    {
        "disease": "痛风", "department": "风湿免疫科",
        "symptoms": ["关节痛", "红肿", "发热", "活动受限"],
        "drugs": ["秋水仙碱", "别嘌醇", "非布司他"],
        "checks": ["血尿酸", "关节X光", "双能CT"],
        "complications": ["痛风石", "肾功能损害"],
        "should_eat": ["低嘌呤饮食", "大量饮水"],
        "avoid_eat": ["海鲜", "动物内脏", "啤酒"],
    },
    {
        "disease": "类风湿关节炎", "department": "风湿免疫科",
        "symptoms": ["关节痛", "晨僵", "肿胀", "乏力", "发热"],
        "drugs": ["甲氨蝶呤", "来氟米特", "托珠单抗"],
        "checks": ["类风湿因子", "抗CCP", "血沉", "X光"],
        "complications": ["关节畸形", "肺间质病变"],
        "should_eat": ["抗炎食物", "深海鱼", "橄榄油"],
        "avoid_eat": ["红肉", "加工食品", "酒精"],
    },
    {
        "disease": "慢性阻塞性肺病", "department": "呼吸内科",
        "symptoms": ["咳嗽", "咳痰", "呼吸困难", "喘息", "乏力"],
        "drugs": ["沙丁胺醇", "噻托溴铵", "布地奈德"],
        "checks": ["肺功能", "胸部CT", "血气分析"],
        "complications": ["呼吸衰竭", "肺心病"],
        "should_eat": ["高蛋白", "易消化"],
        "avoid_eat": ["产气食物", "烟酒"],
    },
    {
        "disease": "哮喘", "department": "呼吸内科",
        "symptoms": ["喘息", "呼吸困难", "咳嗽", "胸闷", "夜间加重"],
        "drugs": ["沙丁胺醇", "布地奈德", "孟鲁司特"],
        "checks": ["肺功能", "过敏原检测", "FeNO"],
        "complications": ["呼吸衰竭", "气胸"],
        "should_eat": ["富含维生素C", "镁"],
        "avoid_eat": ["已知过敏原", "亚硫酸盐食物"],
    },
    {
        "disease": "消化性溃疡", "department": "消化内科",
        "symptoms": ["腹痛", "反酸", "烧心", "恶心", "黑便"],
        "drugs": ["奥美拉唑", "铋剂", "阿莫西林"],
        "checks": ["胃镜", "幽门螺杆菌检测"],
        "complications": ["出血", "穿孔", "梗阻"],
        "should_eat": ["易消化食物", "碱性食物"],
        "avoid_eat": ["辛辣", "酒精", "非甾体抗炎药"],
    },
    {
        "disease": "肝硬化", "department": "消化内科",
        "symptoms": ["乏力", "腹胀", "黄疸", "水肿", "出血倾向"],
        "drugs": ["恩替卡韦", "螺内酯", "乳果糖"],
        "checks": ["肝功能", "腹部B超", "肝活检"],
        "complications": ["腹水", "肝性脑病", "肝癌"],
        "should_eat": ["高蛋白适量", "限盐"],
        "avoid_eat": ["酒精", "粗糙食物"],
    },
    {
        "disease": "胆囊炎", "department": "外科",
        "symptoms": ["腹痛", "恶心", "呕吐", "发热", "黄疸"],
        "drugs": ["头孢曲松", "山莨菪碱", "熊去氧胆酸"],
        "checks": ["腹部B超", "肝功能", "血常规"],
        "complications": ["胆囊穿孔", "胰腺炎"],
        "should_eat": ["低脂饮食", "少量多餐"],
        "avoid_eat": ["高脂", "油炸", "蛋黄"],
    },
    {
        "disease": "阑尾炎", "department": "外科",
        "symptoms": ["腹痛", "恶心", "呕吐", "发热", "食欲减退"],
        "drugs": ["头孢曲松", "甲硝唑", "布洛芬"],
        "checks": ["血常规", "腹部CT", "B超"],
        "complications": ["穿孔", "腹膜炎"],
        "should_eat": ["术后流质", "逐渐过渡"],
        "avoid_eat": ["术前禁食"],
    },
    {
        "disease": "痔疮", "department": "外科",
        "symptoms": ["便血", "疼痛", "瘙痒", "肿物脱出"],
        "drugs": ["马应龙痔疮膏", "地奥司明", "乳果糖"],
        "checks": ["肛门指检", "肠镜"],
        "complications": ["贫血", "嵌顿"],
        "should_eat": ["高纤维", "多饮水"],
        "avoid_eat": ["辛辣", "酒精"],
    },
    {
        "disease": "抑郁症", "department": "精神科",
        "symptoms": ["情绪低落", "失眠", "乏力", "食欲减退", "焦虑", "自杀观念"],
        "drugs": ["舍曲林", "艾司西酞普兰", "文拉法辛"],
        "checks": ["心理评估", "量表测评"],
        "complications": ["自杀", "社会功能损害"],
        "should_eat": ["富含Omega-3", "全谷物", "深色蔬菜"],
        "avoid_eat": ["酒精", "高糖"],
    },
    {
        "disease": "焦虑症", "department": "精神科",
        "symptoms": ["焦虑", "心悸", "出汗", "失眠", "紧张", "头晕"],
        "drugs": ["艾司唑仑", "帕罗西汀", "丁螺环酮"],
        "checks": ["心理评估", "甲状腺功能"],
        "complications": ["抑郁症", "躯体化障碍"],
        "should_eat": ["镁", "B族维生素"],
        "avoid_eat": ["咖啡因", "酒精"],
    },
    {
        "disease": "小儿肺炎", "department": "儿科",
        "symptoms": ["发热", "咳嗽", "喘息", "呼吸急促", "食欲减退"],
        "drugs": ["阿莫西林", "阿奇霉素", "布洛芬"],
        "checks": ["胸部X光", "血常规"],
        "complications": ["呼吸衰竭", "脓胸"],
        "should_eat": ["母乳/配方奶", "易消化"],
        "avoid_eat": ["冷饮", "甜食过多"],
    },
    {
        "disease": "小儿腹泻", "department": "儿科",
        "symptoms": ["腹泻", "呕吐", "发热", "腹痛", "脱水"],
        "drugs": ["口服补液盐", "蒙脱石散", "益生菌"],
        "checks": ["大便常规", "轮状病毒检测"],
        "complications": ["脱水", "电解质紊乱"],
        "should_eat": ["BRAT饮食", "口服补液"],
        "avoid_eat": ["高脂", "高糖"],
    },
    {
        "disease": "小儿哮喘", "department": "儿科",
        "symptoms": ["喘息", "咳嗽", "呼吸困难", "胸闷"],
        "drugs": ["沙丁胺醇", "布地奈德", "孟鲁司特"],
        "checks": ["肺功能", "过敏原检测"],
        "complications": ["呼吸衰竭"],
        "should_eat": ["均衡营养"],
        "avoid_eat": ["已知过敏原"],
    },
    {
        "disease": "月经不调", "department": "妇产科",
        "symptoms": ["月经紊乱", "腹痛", "乏力", "焦虑"],
        "drugs": ["黄体酮", "短效避孕药", "布洛芬"],
        "checks": ["性激素", "妇科B超"],
        "complications": ["不孕", "贫血"],
        "should_eat": ["含铁食物", "均衡饮食"],
        "avoid_eat": ["冷饮", "辛辣"],
    },
    {
        "disease": "子宫肌瘤", "department": "妇产科",
        "symptoms": ["月经量多", "腹痛", "尿频", "贫血"],
        "drugs": ["GnRH激动剂", "米非司酮"],
        "checks": ["妇科B超", "MRI"],
        "complications": ["贫血", "压迫症状"],
        "should_eat": ["含铁", "高蛋白"],
        "avoid_eat": ["雌激素含量高的食物"],
    },
    {
        "disease": "前列腺炎", "department": "泌尿外科",
        "symptoms": ["尿频", "尿急", "尿痛", "会阴痛", "性功能减退"],
        "drugs": ["左氧氟沙星", "α受体阻滞剂", "前列舒通"],
        "checks": ["前列腺液检查", "B超"],
        "complications": ["不育", "慢性盆腔痛"],
        "should_eat": ["番茄", "南瓜子", "锌"],
        "avoid_eat": ["辛辣", "酒精", "久坐"],
    },
    {
        "disease": "脂肪肝", "department": "消化内科",
        "symptoms": ["乏力", "右上腹不适", "肝区胀痛"],
        "drugs": ["多烯磷脂酰胆碱", "水飞蓟素", "二甲双胍"],
        "checks": ["肝功能", "腹部B超", "FibroScan"],
        "complications": ["肝硬化", "肝癌"],
        "should_eat": ["低脂", "高纤维", "控制热量"],
        "avoid_eat": ["酒精", "高糖", "高脂"],
    },
    {
        "disease": "慢性肾炎", "department": "肾内科",
        "symptoms": ["水肿", "血尿", "蛋白尿", "高血压", "乏力"],
        "drugs": ["ACEI/ARB", "激素", "免疫抑制剂"],
        "checks": ["尿常规", "肾功能", "肾活检"],
        "complications": ["尿毒症", "肾性高血压"],
        "should_eat": ["低盐低蛋白", "优质蛋白适量"],
        "avoid_eat": ["高盐", "高钾（晚期）"],
    },
    {
        "disease": "癫痫", "department": "神经内科",
        "symptoms": ["抽搐", "意识丧失", "口吐白沫", "尿失禁"],
        "drugs": ["丙戊酸钠", "左乙拉西坦", "卡马西平"],
        "checks": ["脑电图", "头颅MRI"],
        "complications": ["癫痫持续状态", "意外伤害"],
        "should_eat": ["生酮饮食（部分患者）", "均衡营养"],
        "avoid_eat": ["酒精", "过度疲劳"],
    },
    {
        "disease": "帕金森病", "department": "神经内科",
        "symptoms": ["震颤", "动作迟缓", "肌强直", "平衡障碍"],
        "drugs": ["左旋多巴", "普拉克索", "司来吉兰"],
        "checks": ["神经系统查体", "DAT-PET"],
        "complications": ["痴呆", "跌倒"],
        "should_eat": ["高纤维", "充足水分", "避免高蛋白与药同服"],
        "avoid_eat": ["过量蛋白质（影响左旋多巴吸收）"],
    },
    {
        "disease": "阿尔茨海默病", "department": "神经内科",
        "symptoms": ["记忆力下降", "定向障碍", "语言障碍", "性格改变"],
        "drugs": ["多奈哌齐", "美金刚", "加兰他敏"],
        "checks": ["认知量表", "头颅MRI", "PET"],
        "complications": ["生活不能自理", "感染"],
        "should_eat": ["MIND饮食", "地中海饮食", "坚果"],
        "avoid_eat": ["饱和脂肪", "精制糖"],
    },
    {
        "disease": "系统性红斑狼疮", "department": "风湿免疫科",
        "symptoms": ["皮疹", "关节痛", "发热", "乏力", "光敏感"],
        "drugs": ["羟氯喹", "泼尼松", "环磷酰胺"],
        "checks": ["ANA", "抗dsDNA", "补体"],
        "complications": ["狼疮肾炎", "心血管疾病"],
        "should_eat": ["抗炎饮食", "钙和维生素D"],
        "avoid_eat": ["光敏食物（芹菜等）", "酒精"],
    },
    {
        "disease": "白血病", "department": "血液科",
        "symptoms": ["发热", "贫血", "出血", "淋巴结肿大", "乏力"],
        "drugs": ["化疗方案", "靶向药物", "造血干细胞移植"],
        "checks": ["骨髓穿刺", "流式细胞术", "染色体"],
        "complications": ["感染", "出血", "复发"],
        "should_eat": ["无菌饮食（化疗期）", "高蛋白"],
        "avoid_eat": ["生冷", "未消毒食物"],
    },
    {
        "disease": "艾滋病", "department": "感染科",
        "symptoms": ["发热", "淋巴结肿大", "体重下降", "反复感染", "乏力"],
        "drugs": ["抗逆转录病毒治疗", "复方制剂"],
        "checks": ["HIV抗体", "CD4计数", "病毒载量"],
        "complications": ["机会性感染", "肿瘤"],
        "should_eat": ["均衡营养", "食品安全"],
        "avoid_eat": ["生食", "未消毒"],
    },
    {
        "disease": "结核病", "department": "感染科",
        "symptoms": ["咳嗽", "咳痰", "发热", "盗汗", "体重下降", "乏力"],
        "drugs": ["异烟肼", "利福平", "吡嗪酰胺", "乙胺丁醇"],
        "checks": ["痰涂片", "结核菌培养", "胸部CT"],
        "complications": ["空洞", "咯血", "耐药"],
        "should_eat": ["高蛋白高热量", "充足营养"],
        "avoid_eat": ["酒精（与异烟肼相互作用）"],
    },
    {
        "disease": "带状疱疹", "department": "皮肤科",
        "symptoms": ["皮疹", "疼痛", "水疱", "瘙痒", "发热"],
        "drugs": ["阿昔洛韦", "加巴喷丁", "普瑞巴林"],
        "checks": ["病毒PCR", "临床诊断"],
        "complications": ["后遗神经痛"],
        "should_eat": ["均衡营养", "维生素B"],
        "avoid_eat": ["辛辣", "发物"],
    },
    {
        "disease": "荨麻疹", "department": "皮肤科",
        "symptoms": ["皮疹", "瘙痒", "风团", "红肿"],
        "drugs": ["氯雷他定", "西替利嗪", "糖皮质激素"],
        "checks": ["过敏原检测", "IgE"],
        "complications": ["血管性水肿", "过敏性休克"],
        "should_eat": ["清淡饮食"],
        "avoid_eat": ["已知过敏原", "海鲜", "坚果"],
    },
    {
        "disease": "牙周炎", "department": "口腔科",
        "symptoms": ["牙龈出血", "牙齿松动", "口臭", "疼痛"],
        "drugs": ["甲硝唑", "阿莫西林", "氯己定漱口水"],
        "checks": ["牙周探诊", "X光"],
        "complications": ["牙齿脱落", "全身感染"],
        "should_eat": ["富含维生素C", "钙质"],
        "avoid_eat": [" sticky 食物", "高糖"],
    },
    {
        "disease": "龋齿", "department": "口腔科",
        "symptoms": ["牙痛", "冷热刺激痛", "食物嵌塞"],
        "drugs": ["布洛芬", "氟化物"],
        "checks": ["口腔检查", "X光"],
        "complications": ["牙髓炎", "根尖周炎"],
        "should_eat": ["低糖", "含钙"],
        "avoid_eat": ["高糖", "酸性饮料"],
    },
    {
        "disease": "慢性咽炎", "department": "耳鼻喉科",
        "symptoms": ["咽干", "咽痛", "异物感", "咳嗽", "清嗓"],
        "drugs": ["咽炎片", "雾化吸入", "含片"],
        "checks": ["喉镜检查"],
        "complications": ["慢性化"],
        "should_eat": ["润喉食物", "梨", "蜂蜜"],
        "avoid_eat": ["辛辣", "烟酒", "过烫"],
    },
    {
        "disease": "扁桃体炎", "department": "耳鼻喉科",
        "symptoms": ["咽痛", "发热", "吞咽困难", "扁桃体肿大"],
        "drugs": ["阿莫西林", "布洛芬", "含片"],
        "checks": ["咽拭子培养", "血常规"],
        "complications": ["脓肿", "风湿热"],
        "should_eat": ["流质", "温凉"],
        "avoid_eat": ["辛辣", "过硬食物"],
    },
    {
        "disease": "麦粒肿", "department": "眼科",
        "symptoms": ["眼睑红肿", "疼痛", "异物感"],
        "drugs": ["红霉素眼膏", "热敷"],
        "checks": ["临床诊断"],
        "complications": ["霰粒肿"],
        "should_eat": ["清淡", "维生素A"],
        "avoid_eat": ["辛辣", "油腻"],
    },
    {
        "disease": "青光眼", "department": "眼科",
        "symptoms": ["眼痛", "头痛", "视力模糊", "视野缺损", "恶心呕吐"],
        "drugs": ["噻吗洛尔滴眼液", "毛果芸香碱", "拉坦前列素"],
        "checks": ["眼压", "视野", "OCT"],
        "complications": ["失明"],
        "should_eat": ["均衡饮食"],
        "avoid_eat": ["大量饮水一次", "暗室久待"],
    },
    {
        "disease": "骨质疏松", "department": "骨科",
        "symptoms": ["腰痛", "身高变矮", "骨折", "乏力"],
        "drugs": ["阿仑膦酸钠", "钙剂", "维生素D"],
        "checks": ["骨密度", "骨代谢标志物"],
        "complications": ["脆性骨折"],
        "should_eat": ["高钙", "维生素D", "蛋白质"],
        "avoid_eat": ["过量盐", "咖啡因过量"],
    },
    {
        "disease": "半月板损伤", "department": "骨科",
        "symptoms": [" knee pain", "肿胀", "活动受限", "弹响", "交锁"],
        "drugs": ["塞来昔布", "氨基葡萄糖"],
        "checks": ["MRI", "X光"],
        "complications": ["骨关节炎"],
        "should_eat": ["抗炎食物", "胶原蛋白"],
        "avoid_eat": ["剧烈运动"],
    },
]


def init_graph():
    """初始化Neo4j医疗知识图谱"""
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        # 创建唯一约束
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disease) REQUIRE d.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Symptom) REQUIRE s.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (dep:Department) REQUIRE dep.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (dr:Drug) REQUIRE dr.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Check) REQUIRE c.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (f:Food) REQUIRE f.name IS UNIQUE",
        ]
        for c in constraints:
            try:
                session.run(c)
            except Exception:
                pass

        # 导入数据
        for item in MEDICAL_DATA:
            session.run(
                "MERGE (d:Disease {name: $disease}) "
                "MERGE (dep:Department {name: $department}) "
                "MERGE (d)-[:BELONGS_TO]->(dep)",
                disease=item["disease"], department=item["department"],
            )
            for sym in item["symptoms"]:
                session.run(
                    "MERGE (d:Disease {name: $disease}) "
                    "MERGE (s:Symptom {name: $symptom}) "
                    "MERGE (d)-[:HAS_SYMPTOM]->(s)",
                    disease=item["disease"], symptom=sym,
                )
            for drug in item["drugs"]:
                session.run(
                    "MERGE (d:Disease {name: $disease}) "
                    "MERGE (dr:Drug {name: $drug}) "
                    "MERGE (d)-[:RECOMMEND_DRUG]->(dr)",
                    disease=item["disease"], drug=drug,
                )
            for chk in item["checks"]:
                session.run(
                    "MERGE (d:Disease {name: $disease}) "
                    "MERGE (c:Check {name: $check}) "
                    "MERGE (d)-[:NEED_CHECK]->(c)",
                    disease=item["disease"], check=chk,
                )
            for comp in item.get("complications", []):
                session.run(
                    "MERGE (d1:Disease {name: $disease}) "
                    "MERGE (d2:Disease {name: $comp}) "
                    "MERGE (d1)-[:ACCOMPANY_WITH]->(d2)",
                    disease=item["disease"], comp=comp,
                )
            for food in item.get("should_eat", []):
                session.run(
                    "MERGE (d:Disease {name: $disease}) "
                    "MERGE (f:Food {name: $food}) "
                    "MERGE (d)-[:SHOULD_EAT]->(f)",
                    disease=item["disease"], food=food,
                )
            for food in item.get("avoid_eat", []):
                session.run(
                    "MERGE (d:Disease {name: $disease}) "
                    "MERGE (f:Food {name: $food}) "
                    "MERGE (d)-[:AVOID_EAT]->(f)",
                    disease=item["disease"], food=food,
                )

        # 统计
        result = session.run("MATCH (n) RETURN labels(n)[0] AS label, count(n) AS cnt ORDER BY cnt DESC")
        print("知识图谱导入完成！节点统计：")
        for r in result:
            print(f"  {r['label']}: {r['cnt']}")
    driver.close()


if __name__ == "__main__":
    init_graph()
