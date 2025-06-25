def build_prompt_chain(position, tactical_role):
    print("请回答以下几个问题以生成更适合你的训练建议：\n")
    user_goal = input("你近期最想提升的能力是？（如：抗压持球、前插射门）\n👉 ")
    training_days = input("你每周最多训练几天？（请输入数字，如 3）\n👉 ")
    session_length = input("每次训练大约多长时间？（分钟）\n👉 ")
    training_constraints = input("你在训练上有哪些限制？（如：无队友 / 无器材 / 仅能在家）\n👉 ")
    competition_goal = input("是否有目标比赛或时间节点？（如：两周后校队选拔赛 / 无）\n👉 ")

    user_context = f"""球员基本信息：
- 主位置：{position}
- 战术角色：{tactical_role}

训练需求输入：
- 想提升的能力：{user_goal}
- 每周训练上限：{training_days} 天
- 单次训练时长：{session_length} 分钟
- 训练资源限制：{training_constraints}
- 目标赛事/节点：{competition_goal}
"""

    prompt = f"""


以下是球员信息：
{user_context}

---

---

🎯 请基于上述信息，立即为该球员生成完整的训练建议内容。你必须严格按照以下结构输出：

1️⃣ 本周训练重点建议（结合其想提升的能力）  
2️⃣ 每日训练安排（按时间/频率匹配训练日限制）  
3️⃣ 战术动作结合解释（为什么建议这个训练？比赛中对应什么情境）  
4️⃣ 无资源条件下的替代练法建议  
5️⃣ 一句话总结激励语句（风格像教练）

请直接输出，不需重复前述信息。用中文书写，结构清晰。

"""

    return prompt
