# 🧠 AI Calendar

**Natural Language → Google Calendar**

一个将**自然语言日程描述**自动解析并**添加到 Google Calendar** 的 Python 项目。
支持中文自然语言输入，自动抽取时间、地点与事件信息，并同步到真实日历。

---

## ✨ 功能简介

* 📝 输入一句自然语言

  > 例如：`下周三下午3点在图书馆开组会`

* 🧠 自动解析关键信息

  * 事件名称
  * 开始时间（支持中文相对时间表达）
  * 地点
  * 参与人（可扩展）

* 📅 一键写入 **Google Calendar**

* 🔐 使用 OAuth 2.0，安全访问用户日历

* 🤖 解析逻辑基于大语言模型与规则组合实现

---

## 🛠 技术栈

* **Python 3.9+**
* **Google Calendar API**
* **OAuth 2.0**
* **大语言模型（LLM）**
* `python-dateutil`（时间处理）

---

## 📂 项目结构

```
ai_calendar/
│
├─ event_extractor.py      # 主程序：解析文本并确认添加
├─ calendar_google.py      # Google Calendar API 封装
├─ calendar_writer.py      # 生成 ics 文件
├─ .gitignore              # Git 忽略规则（含密钥）
├─ README.md               # 项目说明
└─ .venv/                  # Python 虚拟环境（不提交）
```

> 文件名可能因实现不同略有差异，不影响整体结构理解。

---

## 🚀 快速开始

### 1️⃣ 克隆项目

```bash
git clone https://github.com/kinster-123/ai-calendar.git
cd ai-calendar
```

---

### 2️⃣ 创建并激活虚拟环境（推荐）

```bash
python -m venv .venv
```

**Windows：**

```bash
.venv\Scripts\activate
```

---

### 3️⃣ 安装依赖

```bash
pip install google-api-python-client google-auth google-auth-oauthlib
pip install python-dateutil requests
```

---

### 4️⃣ 配置 Google Calendar API

1. 在 **Google Cloud Console** 启用 *Google Calendar API*
2. 创建 **OAuth 客户端 ID（桌面应用）**
3. 下载 `client_secret.json`
4. 将其放入项目根目录

⚠️ 该文件 **不会被提交到 GitHub**

---

### 5️⃣ 运行程序

```bash
python event_extractor.py
```

示例交互：

```text
请输入一段自然语言文本：
>>> 下周三下午3点在图书馆开组会

✅ 解析结果：
{
  "title": "组会",
  "start_time": "2026-01-25 15:00:00",
  "location": "图书馆"
}

是否确认添加到日程？(y/n)
>>> y

📅 已成功添加到 Google 日历！
```

---

## ⚠️ 注意事项

* 访问 Google API 需要稳定的网络环境
* 国内网络环境下可能需要代理（如 Clash）
* 请勿将以下文件提交到 GitHub：

  * `client_secret.json`
  * `token.json`

---

## 🌱 可扩展方向

* 更复杂的时间歧义处理
* 多事件解析（一句话包含多个日程）
* 桌面 GUI（PyQt / Tauri）
* 微信 / Telegram 机器人
* 接入 Outlook / Apple Calendar
* 打包为可执行程序（exe）

---

## 📄 License

MIT License

---

## 🙌 致谢

* Google Calendar API
* OpenAI / 大语言模型相关技术

---

**欢迎 Star ⭐ / Fork 🍴 / 提 Issue！**
