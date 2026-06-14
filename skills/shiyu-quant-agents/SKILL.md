---
name: shiyu-quant-agents
description: Apply shiyu-coder's quant and time-series agent frameworks, especially QuantaAlpha self-evolving factor discovery, Kronos financial market foundation-model reasoning, WindFM zero-shot wind-power forecasting, and StochasticGPT stochastic-process modeling. Use for alpha factor generation, quant research, financial time-series forecasting, backtest design, market foundation-model workflows, energy forecasting, and agentic factor mining.
---

# Shiyu Quant Agents

Use this skill as a local Codex wrapper for shiyu-coder's public research projects:

- **QuantaAlpha**: self-evolving LLM factor discovery for quantitative investment.
- **Kronos**: financial market language/foundation-model reasoning for time-series and market prediction tasks.
- **WindFM**: zero-shot wind-power forecasting and energy time-series transfer learning.
- **StochasticGPT**: stochastic-process and probabilistic modeling patterns.

This skill does not execute live trades. Use it for research design, alpha ideation, factor review, forecasting workflows, and backtest planning.

## Core Rule

Separate three things:

- `idea generation`: LLM proposes factors, signals, or model structures;
- `statistical validation`: backtest, IC, RankIC, turnover, drawdown, leakage checks;
- `deployment readiness`: data quality, execution cost, capacity, and monitoring.

Never present an LLM-generated factor as tradable before validation.

## Workflow

1. **Route the task**
   - Factor mining / alpha ideation: use the QuantaAlpha flow.
   - Market time-series forecasting: use the Kronos flow.
   - Energy or wind-power forecasting: use the WindFM flow.
   - Stochastic process modeling: use the StochasticGPT flow.

2. **QuantaAlpha flow**
   - Define universe, frequency, horizon, benchmark, and available data fields.
   - Ask the model to propose candidate factors with:
     `economic intuition -> formula/pseudocode -> required data -> expected regime -> failure mode`.
   - Mutate and refine factors through critique:
     - remove look-ahead leakage;
     - reduce overfitting;
     - simplify expressions;
     - test robustness across sectors, caps, and regimes.
   - Validate with IC/RankIC, long-short return, turnover, max drawdown, capacity, and cost assumptions.

3. **Kronos flow**
   - Treat market prediction as sequence reasoning over price, volume, volatility, events, and regime.
   - Use multi-horizon forecasts: intraday, daily, weekly, and quarterly when data supports it.
   - Report uncertainty, regime sensitivity, and whether the forecast is direction, volatility, or distribution focused.

4. **WindFM flow**
   - For wind/energy tasks, focus on zero-shot or transfer learning:
     `weather context -> turbine/site context -> temporal pattern -> forecast horizon`.
   - Mark domain-shift risk when applying the model to a new geography, turbine type, or weather regime.

5. **StochasticGPT flow**
   - Use stochastic-process language for noisy systems:
     drift, volatility, mean reversion, jump risk, regime switch, diffusion, and tail events.
   - Use it to explain risk and scenario paths, not to overstate precision.

6. **Output**
   - Give candidate factors or forecasts with evidence grade.
   - Include required data, validation plan, and failure modes.
   - For investment tasks, give research priority rather than trading instructions.

## Output Templates

For factor research:

```text
Factor idea:
- Intuition:
- Formula/pseudocode:
- Data required:
- Expected regime:
- Validation metrics:
- Leakage/overfit checks:
- Failure mode:
- Research priority:
```

For forecasting:

```text
Forecast setup:
- Target:
- Horizon:
- Inputs:
- Model lens:
- Expected signal:
- Uncertainty:
- Validation:
- Failure mode:
```

## Sources

- QuantaAlpha: https://github.com/shiyu-coder/QuantaAlpha
- Kronos: https://github.com/shiyu-coder/Kronos
- WindFM: https://github.com/shiyu-coder/WindFM
- StochasticGPT: https://github.com/shiyu-coder/StochasticGPT
