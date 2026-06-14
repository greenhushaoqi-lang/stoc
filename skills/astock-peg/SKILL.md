---
name: astock-peg
description: Apply simonlin1212 astock-peg A-share PEG valuation workflow, localizing Peter Lynch PEG analysis for Chinese stocks. Use when the user asks whether an A-share is cheap/expensive by PEG, growth valuation, EPS growth, consensus growth, PE/G ratio, Peter Lynch style valuation, or A股成长股估值.
---

# Astock PEG

Use this skill as a local Codex wrapper for simonlin1212/astock-peg. It applies PEG valuation to A-shares with local data-source awareness and Chinese-market caveats.

Research only. Do not treat PEG as a standalone trading signal.

## Workflow

1. **Collect current inputs**
   - Current PE, TTM PE, forward PE when available.
   - EPS growth: historical, consensus, and management/industry implied growth.
   - Revenue growth, margin trend, ROE, cash flow, debt, dilution.
   - Industry cycle and policy context.

2. **Calculate PEG**
   - `PEG = PE / EPS growth rate`
   - Use EPS growth as a percentage number. Example: PE 30 and EPS growth 25% gives PEG 1.2.
   - If EPS is negative or cyclical, mark PEG as distorted and use normalized earnings.

3. **A-share adjustments**
   - Discount growth quality when receivables, inventory, or capitalized expenses rise faster than revenue.
   - Discount when profit depends on subsidies, fair-value gains, asset sales, or one-off items.
   - Add caution for ST risk, pledge risk, dilution, unlock pressure, and policy-sensitive sectors.
   - Do not use peak-cycle EPS as normal earnings.

4. **Interpretation**
   - PEG < 0.5: very cheap, verify growth is real.
   - 0.5-1.0: attractive if quality is decent.
   - 1.0-1.5: reasonable.
   - 1.5-2.0: expensive unless growth runway is strong.
   - >2.0: expensive or forecasts too optimistic.

## Output Template

```text
PEG估值结论：

股票：
当前PE：
预期EPS增速：
PEG：

增长质量：
估值档位：
A股调整项：
主要上行驱动：
主要下行风险：
是否适合用PEG：
下一步验证：
```

## Source

Reference project: https://github.com/simonlin1212/astock-peg
