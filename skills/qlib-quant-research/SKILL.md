---
name: qlib-quant-research
description: Apply Microsoft Qlib-inspired AI quant research workflow for alpha research, data processing, model training, backtesting, risk modeling, portfolio optimization, order execution simulation, supervised learning, market dynamics modeling, and reinforcement-learning-style strategy evaluation. Use when the user asks for qlib, AI quant, factor research, backtests, alpha signals, or production-style quant research design.
---

# Qlib Quant Research

Use this skill as a workflow wrapper for Microsoft Qlib: an AI-oriented quant investment platform covering the full chain from data processing and alpha seeking to model training, backtesting, risk modeling, portfolio optimization, and execution simulation.

Do not claim a strategy works without backtest evidence. Keep research, backtest, and live execution separated.

## Workflow

1. **Research question**
   - Define universe, market, frequency, horizon, benchmark, transaction costs, and target metric.

2. **Data layer**
   - Define features, labels, calendar, survivorship handling, corporate actions, missing data, and leakage controls.
   - Prefer clean, point-in-time data for serious conclusions.

3. **Model layer**
   - Choose paradigm:
     - supervised learning for alpha prediction;
     - market dynamics modeling for regime/adaptive behavior;
     - reinforcement-learning-style methods for sequential decision problems.

4. **Backtest layer**
   - Specify train/validation/test split.
   - Include costs, slippage, liquidity limits, turnover, drawdown, and benchmark alpha.
   - Report IC/RankIC, annualized return, Sharpe, max drawdown, turnover, win rate, and capacity caveats when available.

5. **Portfolio layer**
   - Convert signals to weights with risk constraints.
   - Check exposure by sector, factor, liquidity, and concentration.

6. **Production check**
   - State whether the idea is exploratory, backtest-ready, paper-trading-ready, or production-ready.
   - Identify data and engineering blockers.

## Output Template

```text
Qlib-style research plan:

Universe:
Horizon:
Features:
Label:
Model:
Backtest design:
Risk controls:
Metrics:
Expected failure modes:
Next implementation step:
```

## Source

Reference project: https://github.com/microsoft/qlib
