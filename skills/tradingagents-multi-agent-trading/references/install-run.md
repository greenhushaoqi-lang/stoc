# TradingAgents Install And Run Reference

Source repository:

- https://github.com/TauricResearch/TradingAgents
- Chinese mirror page supplied by user: https://www.zdoc.app/zh/TauricResearch/TradingAgents

## Install

Use Python 3.10+.

```powershell
python -m pip install "git+https://github.com/TauricResearch/TradingAgents.git"
```

If working from source:

```powershell
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
python -m pip install -e .
```

The package exposes the CLI command:

```powershell
tradingagents
```

## Key Dependencies

The upstream project uses LangGraph, LangChain provider packages, pandas, yfinance, stockstats, rich, typer, questionary, python-dotenv, requests, and optional provider integrations.

## Configuration

Default home:

```text
~/.tradingagents
```

Common environment variables:

```text
TRADINGAGENTS_LLM_PROVIDER
TRADINGAGENTS_DEEP_THINK_LLM
TRADINGAGENTS_QUICK_THINK_LLM
TRADINGAGENTS_LLM_BACKEND_URL
TRADINGAGENTS_OUTPUT_LANGUAGE
TRADINGAGENTS_MAX_DEBATE_ROUNDS
TRADINGAGENTS_MAX_RISK_ROUNDS
TRADINGAGENTS_CHECKPOINT_ENABLED
TRADINGAGENTS_BENCHMARK_TICKER
TRADINGAGENTS_TEMPERATURE
TRADINGAGENTS_RESULTS_DIR
TRADINGAGENTS_CACHE_DIR
TRADINGAGENTS_MEMORY_LOG_PATH
```

Vendor defaults in v0.2.5:

- core stock APIs: yfinance
- technical indicators: yfinance
- fundamentals: yfinance
- news: yfinance
- macro: FRED, requiring `FRED_API_KEY` for full use
- prediction markets: Polymarket

## Programmatic Pattern

Prefer explicit config:

```python
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"
config["deep_think_llm"] = "gpt-5.5"
config["quick_think_llm"] = "gpt-5.4-mini"
config["output_language"] = "Chinese"
config["max_debate_rounds"] = 1
config["max_risk_discuss_rounds"] = 1

graph = TradingAgentsGraph(
    selected_analysts=["market", "social", "news", "fundamentals"],
    config=config,
)
state, decision = graph.propagate("AAPL", "2026-06-21")
print(decision)
```

Before running, verify upstream constructor signatures against the installed version.

## Operational Notes

- Current data and LLM-provider capabilities change; verify before each serious run.
- For China/Hong Kong tickers, set benchmark explicitly if auto-detection is insufficient.
- Enable checkpointing for long runs if the environment supports SQLite checkpoint storage.
- Keep debate rounds low for quick scans; raise them only for deep research.
