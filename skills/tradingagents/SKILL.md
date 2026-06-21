---
name: tradingagents
category: trading-analysis
description: TradingAgents（TauricResearch，76k★，arXiv 2412.20138）多 Agent LLM 金融交易框架的架构方法论与使用指南。模拟真实交易公司：分析师团队(技术/新闻/情绪/基本面) → 多空研究员结构化辩论 → 研究经理裁决 → 交易员决策 → 风控三方辩论(激进/保守/中立) → 组合经理终审，输出带五档评级的交易决策；内置决策记忆与反思、LangGraph checkpoint。Use when 用户想用多 Agent 辩论流程深度分析某只股票(A股/港股/美股/加密)、理解或复刻"分析师-研究员-交易员-风控-PM"这套投研流水线、配置 deep/quick LLM 与辩论轮数、或安装运行 TradingAgents。
---

## Overview

**TradingAgents** 是一个开源多 Agent LLM 金融交易框架，用一组专业化 LLM agent 模拟真实交易公司的协作与辩论动态，对单只标的在某一日期给出交易决策。**仅供研究，非投资建议。**

- GitHub: https://github.com/TauricResearch/TradingAgents
- 论文: arXiv 2412.20138 · 当前版本 v0.2.5
- 技术栈：Python 3.12 + LangGraph，多 LLM provider（OpenAI/Anthropic/Google/DeepSeek/Qwen/GLM/Grok/Ollama/Bedrock/任意 OpenAI 兼容端点）
- 各 agent 完整系统提示词见 [references/agent-prompts.md](references/agent-prompts.md)

## 一、完整 Agent 流水线（核心方法论）

```
① 分析师团队 Analyst Team（并行产出 4 份报告）
   ├─ 技术分析师 Market：从指标库选≤8个互补指标(MA/MACD/RSI/BOLL/ATR/VWMA…)，分析形态与价格
   ├─ 新闻分析师 News：近一周全球新闻+宏观，解读对市场的影响
   ├─ 情绪分析师 Sentiment：聚合新闻头条/StockTwits/Reddit → 短期市场情绪读数
   └─ 基本面分析师 Fundamentals：财报、公司画像、财务历史 → 内在价值与红旗
            ↓
② 研究团队 Research Team（结构化辩论，max_debate_rounds 轮）
   ├─ 多头研究员 Bull：基于证据强调成长/护城河/正面信号，反驳空头
   ├─ 空头研究员 Bear：强调风险/挑战/负面信号，反驳多头
   └─ 研究经理 Research Manager：批判性裁决辩论，形成投资计划
            ↓
③ 交易员 Trader：综合所有报告 → 决定交易时机与仓位大小，给出方案
            ↓
④ 风控团队 Risk Management（三方辩论，max_risk_discuss_rounds 轮）
   ├─ 激进 Aggressive：争取高收益、高风险敞口
   ├─ 保守 Conservative：保护资本、强调下行
   └─ 中立 Neutral：提供平衡视角
            ↓
⑤ 组合经理 Portfolio Manager：评估风险辩论 → 批准/否决交易方案 → 最终决策（带五档评级）
```

要点：
- **deep_think_llm vs quick_think_llm** 分工：复杂推理(研究经理/PM/辩论)用 deep 模型，常规取数/格式化用 quick 模型，控成本。
- **辩论是核心**：多空 + 风控三方的对抗式辩论，比单一 agent 更能暴露盲点。
- **结构化输出 agent**：Research Manager / Trader / Portfolio Manager 产出结构化决策（v0.2.4+），含五档评级（v0.2.2+）。

## 二、决策记忆与反思（持续学习机制）

决策日志默认常开，每次运行把决策追加到 `~/.tradingagents/memory/trading_memory.md`。**同一标的下次运行时**：框架取回上次的已实现收益（原始 + 相对 SPY 的 alpha），生成一段反思，并把该标的最近的决策 + 跨标的近期教训注入 PM 提示词——让每次分析携带"上次什么管用/不管用"。路径可用 `TRADINGAGENTS_MEMORY_LOG_PATH` 覆盖。

**Checkpoint 续跑**：`--checkpoint` 开启后 LangGraph 每个节点存盘，崩溃/中断可从最后成功步恢复（日志显示 `Resuming from step N`），成功完成后自动清理。

## 三、安装与运行

```bash
git clone https://github.com/TauricResearch/TradingAgents.git && cd TradingAgents
conda create -n tradingagents python=3.12 && conda activate tradingagents
pip install .                      # 或 Docker: cp .env.example .env && docker compose run --rm tradingagents
```

需在 `.env` 配置对应 provider 的 API key（框架会自动探测）。

### CLI（交互式）
```bash
tradingagents          # 安装后命令；或 python -m cli.main
```
交互选择：标的、分析日期、LLM provider、研究深度等。

### 编程调用
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
config["llm_provider"]   = "openai"        # openai/google/anthropic/deepseek/groq/ollama/openai_compatible
config["deep_think_llm"] = "gpt-5.5"       # 复杂推理模型
config["quick_think_llm"]= "gpt-5.4-mini"  # 快速任务模型
config["max_debate_rounds"] = 2            # 多空辩论轮数

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2026-01-15")   # 返回最终决策
print(decision)
```

## 四、支持的市场与代码（用 Yahoo Finance 后缀）

| 市场 | 示例 |
| --- | --- |
| 美股 | `AAPL`、`SPY` |
| 港股 / 东京 / 伦敦 | `0700.HK` / `7203.T` / `AZN.L` |
| A 股 | 上海 `600519.SS`（茅台）、深圳 `.SZ` |
| 印度/加/澳 | `RELIANCE.NS`/`.BO`、`.TO`、`.AX` |
| 加密 | `BTC-USD`、`ETH-USD` |

公司身份与 alpha 基准按市场自动解析。

## 五、关键配置（`TRADINGAGENTS_*` 环境变量可覆盖）

| config key / env | 说明 |
| --- | --- |
| `llm_provider` / `TRADINGAGENTS_LLM_PROVIDER` | LLM 提供商 |
| `deep_think_llm` / `quick_think_llm` | 深/浅思考模型 |
| `backend_url` / `TRADINGAGENTS_LLM_BACKEND_URL` | OpenAI 兼容端点（vLLM/LM Studio/Ollama/llama.cpp） |
| `max_debate_rounds` / `max_risk_discuss_rounds` | 研究/风控辩论轮数 |
| `output_language` | 输出语言（多语言支持） |
| `benchmark_ticker` | alpha 基准（默认按市场，美股 SPY） |
| `temperature` | 采样温度 |

本地模型：`llm_provider: "ollama"`（默认 `http://localhost:11434/v1`，远程设 `OLLAMA_BASE_URL`）。AWS Bedrock：`pip install ".[bedrock]"`，模型如 `us.anthropic.claude-opus-4-8-v1:0`。

## 如何用这个 skill

- 用户要"深度分析某股" → 按 ①→⑤ 流水线组织分析：先出 4 份分析师报告，再走多空辩论→研究经理裁决→交易员方案→风控三方辩论→PM 终审决策（给五档评级）。可不安装框架，直接用这套方法论手动跑。
- 用户要真跑框架 → 给安装命令 + `propagate(ticker, date)` 示例 + provider/辩论轮数配置。
- 需要某个 agent 的原版提示词 → 见 [references/agent-prompts.md](references/agent-prompts.md)。
- 关联：PanWatch（[[panwatch]]）正是把本框架接入盯盘 App 的实例。

## 免责声明

TradingAgents 为研究用途，交易表现受模型、温度、周期、数据质量等多因素影响，不构成财务/投资/交易建议。
