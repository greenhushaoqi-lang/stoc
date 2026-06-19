# TauricResearch Source Map

Last learned: 2026-06-19

## GitHub Organization

- Organization: `https://github.com/TauricResearch`
- Public repositories checked:
  - `TradingAgents`: full multi-agent LLM trading research framework.
  - `Trading-R1`: README-only public placeholder at the checked snapshot; no installable terminal code was present.
  - `.github`: organization profile/config repository; no market-research skill or agent logic identified.

## TradingAgents

- Repo: `https://github.com/TauricResearch/TradingAgents`
- Snapshot learned: `c15200dc286b66abce3f1bcf09b298dc06b8539d`
- README version signal: TradingAgents v0.2.5 release notes mention grounded sentiment analyst, expanded model/provider coverage, `TRADINGAGENTS_*` env overrides, non-US alpha benchmarks, and ticker path hardening.
- Core package path: `tradingagents/`
- Agent path: `tradingagents/agents/`
- Graph path: `tradingagents/graph/`
- Default config path: `tradingagents/default_config.py`

### Installed Interpretation

This Codex skill does not vendor the full TradingAgents Python package. It installs the framework logic as a reusable research workflow:

1. Market analyst.
2. Sentiment analyst.
3. News analyst.
4. Fundamentals analyst.
5. Bull researcher.
6. Bear researcher.
7. Research manager.
8. Trader proposal.
9. Aggressive risk analyst.
10. Neutral risk analyst.
11. Conservative risk analyst.
12. Portfolio-manager synthesis.
13. Trading-R1 grounding/risk-adjusted reasoning pass.

When a user asks to run the actual Tauric Python framework, clone or install `TradingAgents` separately and provide the required API keys. For normal Codex stock research, use this skill as the orchestration protocol and combine it with local A-share, global market, news, X/Xueqiu/Taoguba, and finance data skills.

## Trading-R1

- Repo: `https://github.com/TauricResearch/Trading-R1`
- Snapshot learned: `57810bfb4456ba1509a2a3c6d502d3085922bf83`
- Public content at snapshot: `README.md` with `# Trading-R1` and `Releasing soon: Trading-R1 Terminal`.
- Installability: no executable agent code, package, skill, or terminal implementation was present in the public repository at the checked snapshot.

### Installed Interpretation

Use Trading-R1 here as a reasoning discipline:

- thesis completeness;
- facts-grounded evidence separation;
- counterfactual checks;
- volatility, drawdown, liquidity, crowding, and event-gap adjustment;
- explicit invalidation and missing-proof fields.

Do not claim the Trading-R1 terminal has been installed unless the public repository later ships code and it is installed separately.

## Update Rule

If TauricResearch releases new code, re-run repository discovery and update this source map with:

- repository name;
- commit hash;
- files inspected;
- whether it contains installable code, a Codex skill, or agent definitions;
- what changed in the local skill.
