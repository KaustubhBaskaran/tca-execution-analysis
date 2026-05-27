# Transaction Cost Analysis — Multi-Asset Execution Quality

## Overview
This project implements a Transaction Cost Analysis (TCA) framework to measure and compare execution quality across five liquid U.S. equities and ETFs: AAPL, GOOGL, JPM, MSFT, and SPY.

TCA is a critical tool used by institutional broker-dealers and buyside firms to evaluate trading performance, minimize execution costs, and optimize algorithmic strategies.

## Metrics Analyzed
- **Slippage** — difference between arrival price (open) and execution price (VWAP proxy), in basis points
- **Spread Proxy** — intraday high-low range as a percentage of close, capturing liquidity cost
- **Market Impact** — price movement relative to volume, measuring how much a trade moves the market
- **Implementation Shortfall (IS)** — difference between decision price (prior close) and execution price, the most widely used institutional TCA benchmark

## Key Findings
- SPY exhibited the lowest execution costs across all metrics, consistent with its status as the most liquid U.S. equity instrument
- GOOGL showed the highest average slippage (6.97 bps) and widest spread proxy (240 bps), reflecting higher volatility and wider bid-ask spreads
- JPM and MSFT demonstrated negative average Implementation Shortfall, indicating executions that outperformed the decision price on average
- MSFT showed the highest IS standard deviation (161 bps), suggesting inconsistent execution quality despite favorable average outcomes

## Tools & Technologies
- **Python** — pandas, numpy, matplotlib, seaborn, yfinance, openpyxl
- **Data Source** — Yahoo Finance (6 months of daily OHLCV data)
- **Output** — Visualizations (PNG) and Excel summary report

## Project Structure
\```
tca-execution-analysis/
│
├── tca_analysis.py          
├── visuals/
│   ├── tca_dashboard.png           
│   └── implementation_shortfall.png 
├── reports/
│   └── tca_summary_report.xlsx     
└── README.md
\```

## How to Run
```bash
git clone https://github.com/KaustubhBaskaran/tca-execution-analysis
cd tca-execution-analysis
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python tca_analysis.py
```

## Context
Built as part of ongoing learning in algorithmic trading and execution analytics, with a focus on the tools and metrics used by institutional broker-dealers in multi-asset execution environments.