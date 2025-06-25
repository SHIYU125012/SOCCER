def build_generation_prompt(data, lang_code="C"):
    prompt_templates = {
        "C": """
你是一位擅长为学生运动员设计训练计划的专业足球教练。
请根据以下球员信息与需求，为其制定【个性化训练建议】，内容包括：

1️⃣ 本周训练重点建议（结合其想提升的能力）
2️⃣ 每日训练安排（按时间/频率匹配训练日限制）
3️⃣ 战术动作结合解释（为什么建议这个训练？比赛中对应什么情境）
4️⃣ 无资源条件下的替代练法建议
5️⃣ 一句话总结激励语句（风格像教练）

以下是球员信息：
- 主位置：{position}
- 战术角色：{tactical_role}
- 想提升的能力：{user_goal}
- 每周训练天数：{training_days} 天
- 单次训练时长：{session_length} 分钟
- 训练资源限制：{training_constraints}
- 目标赛事/节点：{competition_goal}

---

🎯 请立即开始输出训练建议。请用中文书写，结构清晰。
""",

        "E": """
You are a professional football coach specializing in training plans for student athletes.
Based on the player's information below, generate a **personalized weekly training recommendation**. The output should include:

1️⃣ Weekly training priorities (based on development goal)
2️⃣ Suggested daily schedule (based on frequency/duration limits)
3️⃣ Tactical reasoning (why this training helps in match conditions)
4️⃣ Alternative drills (in case of no partners/equipment)
5️⃣ One-sentence coaching summary (like a motivational coach)

Player info:
- Position: {position}
- Tactical Role: {tactical_role}
- Development Goal: {user_goal}
- Training Days/Week: {training_days} days
- Session Length: {session_length} minutes
- Constraints: {training_constraints}
- Target Event: {competition_goal}

---

🎯 Begin your recommendation now. Respond in English, well-structured and coach-style.
""",

        "J": """
あなたは学生アスリートのためのサッカー専門コーチです。
以下の選手情報に基づき、個別の【1週間トレーニング提案】を日本語で出力してください。構成は以下の通り：

1️⃣ 今週の重点トレーニング（強化したい能力に基づく）
2️⃣ 日毎の練習メニュー（頻度と時間制限に配慮）
3️⃣ 戦術的な理由説明（なぜこれを行うか、どの試合場面を想定しているか）
4️⃣ 器具や味方がない場合の代替練習
5️⃣ 一言でのモチベーションアップコメント（コーチ風）

選手情報：
- ポジション：{position}
- 戦術ロール：{tactical_role}
- 強化目標：{user_goal}
- 週間練習日数：{training_days} 日
- 1回あたりの練習時間：{session_length} 分
- 制約条件：{training_constraints}
- ターゲット大会・時期：{competition_goal}

---

🎯 すぐに提案文を日本語で出力してください。構成は明確にしてください。
"""
    }

    template = prompt_templates.get(lang_code, prompt_templates["C"])
    return template.format(**data)


