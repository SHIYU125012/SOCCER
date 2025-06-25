import streamlit as st
import json
import openai

# ✅ 直接写入你的 OpenAI 密钥（替换成你自己的 key）
openai.api_key = "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"

# 读取角色映射字典
with open("./config/ROLE_MAP_MULTILINGUAL.json", "r", encoding="utf-8") as f:
    ROLE_MAP = json.load(f)

LANG_OPTIONS = {"中文": "C", "English": "E", "日本語": "J"}

LANG_TEXTS = {
    "C": {
        "title": "⚽ GPTCoach - 学生运动员个性化训练建议生成器",
        "intro": "本工具基于 GPT，旨在为学生运动员提供结合位置与角色的个性化训练建议。请根据提示依次填写。",
        "select_lang": "请选择语言 / Language / 言語",
        "select_position": "请选择主位置：",
        "select_role": "请选择你的战术角色类型：",
        "section_training": "📋 训练目标与限制",
        "goal": "你近期最想提升的能力是？（如：抗压持球、前插射门）",
        "days": "你每周最多训练几天？",
        "minutes": "每次训练大约多长时间（分钟）？",
        "constraints": "你在训练上有哪些限制？（如：无队友 / 无器材 / 仅能在家）",
        "event": "是否有目标比赛或时间节点？（如：两周后校队选拔赛 / 无）",
        "generate": "🎯 生成训练建议",
        "output": "### 🧠 GPT 训练建议输出：",
        "error": "生成失败："
    },
    "E": {
        "title": "⚽ GPTCoach - Personalized Training Generator for Student Athletes",
        "intro": "This tool uses GPT to generate personalized training advice for student athletes based on their position and role. Please fill in the form below.",
        "select_lang": "Select Language / 言語 / 语言",
        "select_position": "Select Primary Position:",
        "select_role": "Select Your Tactical Role:",
        "section_training": "📋 Training Goals and Constraints",
        "goal": "What skill do you most want to improve now? (e.g., ball retention, finishing)",
        "days": "How many days per week can you train?",
        "minutes": "How long is each session (minutes)?",
        "constraints": "Any training limitations? (e.g., no partner/equipment/home only)",
        "event": "Do you have a goal match/event? (e.g., school tryout in 2 weeks / None)",
        "generate": "🎯 Generate Training Plan",
        "output": "### 🧠 GPT Training Recommendation Output:",
        "error": "Generation failed:"
    },
    "J": {
        "title": "⚽ GPTCoach - 学生アスリート向け個別トレーニング提案生成器",
        "intro": "このツールは、選手のポジションや役割に応じて個別のトレーニング提案を GPT で生成します。以下の情報を入力してください。",
        "select_lang": "言語を選択 / Select Language / 语言",
        "select_position": "主なポジションを選んでください：",
        "select_role": "自分の戦術ロールを選んでください：",
        "section_training": "📋 トレーニング目標と制約",
        "goal": "最近特に向上させたいスキルは？（例：ボール保持、フィニッシュ）",
        "days": "週に何日練習できますか？",
        "minutes": "1回の練習時間（分）は？",
        "constraints": "トレーニングに関する制約はありますか？（例：器具なし、自宅のみなど）",
        "event": "目標となる大会や時期はありますか？（例：2週間後の選抜試験／なし）",
        "generate": "🎯 トレーニング提案を生成",
        "output": "### 🧠 GPT トレーニング提案出力：",
        "error": "生成に失敗しました："
    }
}

def run_ui():
    st.set_page_config(page_title="Student-Athlete GPTCoach", layout="wide")

    lang_name = st.selectbox("Language / 言語 / 语言", list(LANG_OPTIONS.keys()))
    lang_code = LANG_OPTIONS[lang_name]
    text = LANG_TEXTS[lang_code]

    st.title(text["title"])
    st.markdown(text["intro"])

    # 主位置选择
    position_options = [(v["code"], k) for k, v in ROLE_MAP.items()]
    position_dict = {v: k for v, k in position_options}
    position_code = st.selectbox(text["select_position"], [v for v, _ in position_options])
    selected_idx = position_dict[position_code]

    # 战术角色子类型
    tactical_roles = ROLE_MAP[selected_idx]["subtypes"][lang_code]
    selected_role = st.selectbox(text["select_role"], tactical_roles)

    st.markdown("---")
    st.subheader(text["section_training"])

    user_goal = st.text_input(text["goal"])
    training_days = st.number_input(text["days"], min_value=1, max_value=7, step=1)
    session_length = st.number_input(text["minutes"], min_value=10, max_value=180, step=5)
    training_constraints = st.text_area(text["constraints"])
    competition_goal = st.text_input(text["event"])

    st.markdown("---")
    if st.button(text["generate"]):
        user_data = {
            "position": position_code,
            "tactical_role": selected_role,
            "user_goal": user_goal,
            "training_days": training_days,
            "session_length": session_length,
            "training_constraints": training_constraints,
            "competition_goal": competition_goal
        }

        prompt = build_generation_prompt(user_data, lang_code)

        st.markdown(text["output"])
        try:
            gpt_reply = generate_gpt_response(prompt)
            st.success("✅")
            st.markdown(gpt_reply)
        except Exception as e:
            st.error(f"{text['error']}\n\n{e}")

# ⚠️ 保持原始的 Prompt 模板定义不变

def build_generation_prompt(data, lang_code="C"):
    prompts = {
        "C": f"""
你是一位具有10年执教经验的职业足球教练，专注于青少年和学生运动员的个性化成长训练。

请根据以下球员信息，为其制定【本周训练建议】，要求结合其训练目标与资源限制，建议务实可行，结构清晰。

球员信息：
- 主位置：{data['position']}
- 战术角色：{data['tactical_role']}
- 想提升的能力：{data['user_goal']}
- 每周训练天数：{data['training_days']} 天
- 单次训练时长：{data['session_length']} 分钟
- 训练资源限制：{data['training_constraints']}
- 目标比赛/时间节点：{data['competition_goal']}

请按照如下格式输出：

📌 本周训练重点建议：
...

📅 每日训练安排（每次训练{data['session_length']}分钟以内）：
- 周一：...
- 周二：...
...

🎯 战术动作与比赛情境说明：
...

🔁 替代练法建议（无队友/器材时）：
...

💬 教练式激励语（一句话）：
...

语言要求：中文，风格专业、清晰，表达像真实教练。
""",

        "E": f"""
You are a professional football coach with over 10 years of experience, specializing in personalized training for student athletes.

Based on the player information below, generate a practical and structured **weekly training recommendation**.

Player info:
- Position: {data['position']}
- Tactical Role: {data['tactical_role']}
- Development Goal: {data['user_goal']}
- Available Days/Week: {data['training_days']} days
- Max Session Length: {data['session_length']} minutes
- Constraints: {data['training_constraints']}
- Target Event: {data['competition_goal']}

Please follow this structure:

📌 Weekly Focus:
...

📅 Daily Plan (no more than {data['session_length']} minutes/session):
- Monday: ...
- Tuesday: ...
...

🎯 Tactical Reasoning:
...

🔁 Alternative Drills (no partners/equipment):
...

💬 Motivational Coaching Summary (1 sentence):
...

Language: English, professional and clear, like a real coach.
""",

        "J": f"""
あなたは10年以上の指導経験を持つサッカー専門コーチで、学生アスリート向けの個別トレーニングを得意としています。

以下の選手情報に基づき、現実的かつ構造的な【1週間のトレーニング提案】を出力してください。

選手情報：
- ポジション：{data['position']}
- 戦術ロール：{data['tactical_role']}
- 強化目標：{data['user_goal']}
- 週の練習可能日数：{data['training_days']} 日
- 1回あたりの練習時間：{data['session_length']} 分以内
- 制約条件：{data['training_constraints']}
- 目標大会・時期：{data['competition_goal']}

以下の構成で出力してください：

📌 今週の重点トレーニング：
...

📅 日別メニュー（1回{data['session_length']}分以内）：
- 月曜日：...
- 火曜日：...
...

🎯 戦術的な意図と試合状況：
...

🔁 代替練習（器具なし・味方なし時）：
...

💬 コーチからの激励メッセージ（一言）：
...

言語：日本語。トーンはプロのコーチのように明確かつ温かく。
"""
    }
    return prompts.get(lang_code, prompts["C"])

def generate_gpt_response(prompt, model="gpt-4o"):
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一位训练经验丰富的足球教练，擅长为学生运动员制定训练计划。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2048
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    run_ui()
