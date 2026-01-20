import json
from datetime import datetime
from typing import Optional, List, Literal
from calendar_writer import write_event_to_ics

from pydantic import BaseModel, ValidationError
from dateutil import parser
from openai import OpenAI
from calendar_google import insert_event_to_google_calendar

# =========================
# 1. 配置你的 API Key
# =========================
client = OpenAI()

# =========================
# 2. 定义结构化 Schema
# =========================
class Event(BaseModel):
    title: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    location: Optional[str]
    participants: List[str]
    confidence: Literal["high", "medium", "low"]
    original_text: str


# =========================
# 3. Prompt 模板
# =========================
PROMPT_TEMPLATE = """
你是一个“日程信息抽取器”。

请从下面的文本中，判断是否包含一个明确、可记录为日程的事件。
如果有，请严格按 JSON 格式返回以下字段：
title、start_time、end_time、location、participants、confidence、original_text

要求：
1. 时间请转换为 ISO-8601 格式（例如 2026-01-21T15:00）
2. 如果时间无法确定，请返回 null
3. 不要输出任何解释性文字
4. 只输出一个 JSON 对象
5. participants 字段始终为数组

时间解释规则：
1. “下周X”指的是“下一个自然周（周一开始）中的星期X”
2. 一周从周一开始，到周日结束
3. 所有时间基于中国标准时间（UTC+8）

当前时间是：{now}

文本：
{user_text}
"""

# =========================
# 4. 调用 LLM 抽取事件
# =========================
def extract_event(text: str) -> Event:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    prompt = PROMPT_TEMPLATE.format(
        now=now,
        user_text=text
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 可换成你自己的模型
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        data = json.loads(raw_output)
        # ===== 修正 confidence =====
        conf = data.get("confidence")

        if isinstance(conf, int):
            data["confidence"] = (
                "high" if conf >= 2 else "medium"
            )
        elif isinstance(conf, str):
            conf = conf.lower()
            if conf not in ("high", "medium", "low"):
                data["confidence"] = "medium"
        else:
            data["confidence"] = "medium"
    except json.JSONDecodeError:
        raise ValueError("模型输出不是合法 JSON：\n" + raw_output)

    try:
        return Event(**data)
    except ValidationError as e:
        raise ValueError("JSON 结构不符合预期：\n" + str(e))


# =========================
# 5. 简单时间合理性校验
# =========================
def validate_time(event: Event):
    if event.start_time and event.end_time:
        if event.end_time <= event.start_time:
            raise ValueError("结束时间早于开始时间")


# =========================
# 6. 主程序入口
# =========================
def main():
    print("请输入一段自然语言文本（例如：下周三下午3点在图书馆开组会）：\n")
    text = input(">>> ")

    try:
        event = extract_event(text)
        validate_time(event)
    except Exception as e:
        print("\n❌ 解析失败：")
        print(e)
        return

    print("\n✅ 解析结果：\n")
    print(json.dumps(event.model_dump(), ensure_ascii=False, indent=2, default=str))

    print("\n是否确认添加到日程？(y/n)")
    confirm = input(">>> ").lower()

    if confirm == "y":
        link = insert_event_to_google_calendar(event)
        print("📅 已成功添加到 Google 日历！")
        print(f"🔗 日程链接：{link}")
    else:
        print("\n🚫 已取消")

if __name__ == "__main__":
    main()
