import json
import time

# ==========================================
# 模块 1：模拟外部工具与知识库 (Tools & RAG)
# ==========================================
def tool_search_safety_regulations(keyword):
    """
    规程检索 Agent (RAG) 调用的工具：模拟从《煤矿安全规程》知识库中检索相关条款
    """
    print(f"    [系统] 正在知识库中检索关于 '{keyword}' 的安全规程...")
    time.sleep(1) # 模拟检索延迟
    
    knowledge_base = {
        "主通风机": "《煤矿安全规程》第一百五十八条：主要通风机必须安装在地面；装有主要通风机的出风井口应安装防爆门，防爆门每6个月检查维修1次。",
        "带式输送机": "《煤矿安全规程》第三百七十三条：采用滚筒驱动带式输送机运输时，必须装设防滑、防跑偏、防撕裂、防烟雾、超温洒水装置。",
        "瓦斯": "《煤矿安全规程》第一百八十条：矿井总回风巷或一翼回风巷中瓦斯或二氧化碳浓度超过0.75%时，必须立即查明原因，进行处理。"
    }
    
    # 模糊匹配
    for key, rule in knowledge_base.items():
        if key in keyword or keyword in key:
            return rule
    return "未检索到明确的专项规程，请参考通用工业安全生产标准执行。"

# ==========================================
# 模块 2：定义核心 Agents
# ==========================================

def agent_data_analyzer(raw_log):
    """
    Agent 1: 现场数据分析 Agent
    负责解析非结构化的巡检日志，提取核心故障特征和设备对象。
    """
    print("▶ [Agent 1: 数据分析专家] 正在解析现场巡检日志...")
    # 这里在真实场景中是调用 LLM 解析，此处我们模拟 LLM 的结构化输出
    # 假设 LLM 已经阅读了 raw_log 并提取了关键信息
    
    analyzed_data = {
        "device_target": "带式输送机",
        "abnormal_phenomenon": "驱动滚筒处温度异常升高，且现场伴有轻微焦糊味；防滑保护传感器显示离线。",
        "severity_guess": "High"
    }
    time.sleep(1)
    print(f"  √ 解析完成：锁定目标设备为 '{analyzed_data['device_target']}'")
    return analyzed_data


def agent_compliance_retriever(analyzed_data):
    """
    Agent 2: 合规审查 Agent
    根据分析出的设备，自动调用 RAG 工具获取对应的安全法规。
    """
    print("▶ [Agent 2: 合规审查专家] 正在匹配安全规程与法律法规...")
    target = analyzed_data.get("device_target", "")
    
    # Agent 决定调用搜索工具
    regulation = tool_search_safety_regulations(target)
    
    analyzed_data["matched_regulation"] = regulation
    print(f"  √ 匹配完成：找到关联条款")
    return analyzed_data


def agent_decision_maker(context_data):
    """
    Agent 3: 专家决策与报告 Agent (包含 CoT 长链推理逻辑)
    综合现场情况和法规，进行思维链推理，出具最终的整改报告。
    """
    print("▶ [Agent 3: 专家决策组] 启动思维链 (CoT) 推理并生成最终报告...")
    time.sleep(1.5)
    
    # 模拟思维链 (Chain of Thought) 推理过程
    reasoning_process = f"""
    推理步骤 1：现场设备为 {context_data['device_target']}，异常为 {context_data['abnormal_phenomenon']}。
    推理步骤 2：比对规程 `{context_data['matched_regulation']}`。规程要求必须装设防烟雾、超温洒水及防滑装置。
    推理步骤 3：现状指出“防滑保护传感器离线”且“温度异常升高”，这构成了对规程第三百七十三条的实质性违反。
    推理步骤 4：由于伴有焦糊味，存在引发矿井火灾（极高危）的潜在风险，必须立即停机整改。
    """
    
    report = f"""
==================================================
        智慧矿山现场安全隐患诊断报告 (AI生成)
==================================================
【告警等级】 🔴 极高风险 (立即停机)
【涉事设备】 {context_data['device_target']}

【隐患描述】
{context_data['abnormal_phenomenon']}

【违反合规条款】
{context_data['matched_regulation']}

【AI 专家整改建议 (知行合一闭环执行)】
1. 立即停止该带式输送机的运行，切断驱动电机电源。
2. 派遣电气工程师排查防滑保护传感器离线原因（检查线路压降或通信模块）。
3. 检查并清理滚筒处堆积的煤粉，查明温度升高是机械摩擦还是电机过载导致。
4. 验证超温洒水装置是否处于就绪状态。

【系统推理日志】
{reasoning_process}
==================================================
"""
    return report

# ==========================================
# 模块 3：主工作流编排 (Workflow Orchestration)
# ==========================================

def run_smart_mine_workflow(inspection_log):
    """主调度函数：将业务逻辑串联起来"""
    print(f"\n[系统接入] 收到前端传来的现场巡检语音/文本记录：\n'{inspection_log}'\n")
    print("-" * 50)
    
    # 步骤 1：数据提取
    step1_result = agent_data_analyzer(inspection_log)
    
    # 步骤 2：规程匹配
    step2_result = agent_compliance_retriever(step1_result)
    
    # 步骤 3：推理与报告生成
    final_report = agent_decision_maker(step2_result)
    
    print(final_report)
    return final_report

# ==========================================
# 执行测试
# ==========================================
if __name__ == "__main__":
    # 模拟一线工人输入的现场记录
    mock_input = "报告调度室，二号井下主巷道的皮带机现在好像有点问题，驱动那块儿特别烫，能闻到糊味，而且我看那个防滑传感器的灯不亮了，好像掉线了。"
    run_smart_mine_workflow(mock_input)