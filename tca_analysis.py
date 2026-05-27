import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. Pull Data ──────────────────────────────────────────────────────────────
tickers = ['SPY', 'AAPL', 'MSFT', 'GOOGL', 'JPM']
raw = yf.download(tickers, period='6mo', interval='1d', auto_adjust=True)

# Extract OHLCV
close  = raw['Close']
open_  = raw['Open']
high   = raw['High']
low    = raw['Low']
volume = raw['Volume']

# ── 2. Core TCA Metrics ───────────────────────────────────────────────────────

# Daily return
returns = close.pct_change().dropna()

# Arrival price = open (simulating order placed at market open)
arrival_price = open_

# Execution price = VWAP proxy: (High + Low + Close) / 3
vwap = (high + low + close) / 3

# Slippage = (execution price - arrival price) / arrival price
slippage = (vwap - arrival_price) / arrival_price * 10000  # in basis points

# Spread proxy = (High - Low) / Close * 10000 (basis points)
spread = (high - low) / close * 10000

# Market impact proxy = abs(return) / log(volume)
log_vol = np.log(volume.replace(0, np.nan))
market_impact = (returns.abs() / log_vol) * 10000

print("=== TCA Summary (basis points) ===")
print("\nAverage Slippage (bps):")
print(slippage.mean().round(2))
print("\nAverage Spread Proxy (bps):")
print(spread.mean().round(2))
print("\nAverage Market Impact (bps):")
print(market_impact.mean().round(2))

# ── 3. Visualizations ─────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(3, 1, figsize=(12, 14))
fig.suptitle("Transaction Cost Analysis — Multi-Asset Execution Quality", 
             fontsize=16, fontweight='bold', y=1.01)

# Plot 1: Average Slippage by Ticker
slippage.mean().plot(kind='bar', ax=axes[0], color='steelblue', edgecolor='black')
axes[0].set_title("Average Slippage by Ticker (bps)")
axes[0].set_ylabel("Basis Points")
axes[0].set_xlabel("")
axes[0].axhline(0, color='red', linestyle='--', linewidth=1)

# Plot 2: Spread Proxy Over Time
spread.plot(ax=axes[1], linewidth=1.2)
axes[1].set_title("Daily Spread Proxy Over Time (bps)")
axes[1].set_ylabel("Basis Points")
axes[1].set_xlabel("")
axes[1].legend(tickers, loc='upper right')

# Plot 3: Market Impact by Ticker
market_impact.mean().plot(kind='bar', ax=axes[2], color='coral', edgecolor='black')
axes[2].set_title("Average Market Impact by Ticker (bps)")
axes[2].set_ylabel("Basis Points")
axes[2].set_xlabel("")

plt.tight_layout()
plt.savefig("visuals/tca_dashboard.png", dpi=150, bbox_inches='tight')
plt.show()
print("\nChart saved to visuals/tca_dashboard.png")

# ── 4. Implementation Shortfall ───────────────────────────────────────────────
# IS = (Final Execution Price - Decision Price) / Decision Price
# We simulate: decision price = previous day close, execution = next day VWAP

decision_price = close.shift(1)
execution_price = vwap

implementation_shortfall = (execution_price - decision_price) / decision_price * 10000

print("\n=== Implementation Shortfall (bps) ===")
print("\nMean IS:")
print(implementation_shortfall.mean().round(2))
print("\nStd Dev IS (execution consistency):")
print(implementation_shortfall.std().round(2))

# Plot IS distribution
fig, axes = plt.subplots(1, 5, figsize=(18, 4))
fig.suptitle("Implementation Shortfall Distribution by Ticker (bps)", 
             fontsize=14, fontweight='bold')

for i, ticker in enumerate(tickers):
    axes[i].hist(implementation_shortfall[ticker].dropna(), 
                 bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    axes[i].axvline(implementation_shortfall[ticker].mean(), 
                    color='red', linestyle='--', linewidth=1.5, label='Mean')
    axes[i].set_title(ticker)
    axes[i].set_xlabel("bps")
    axes[i].set_ylabel("Frequency" if i == 0 else "")

plt.tight_layout()
plt.savefig("visuals/implementation_shortfall.png", dpi=150, bbox_inches='tight')
plt.show()
print("\nChart saved to visuals/implementation_shortfall.png")

# ── 5. Export Summary Report to Excel ─────────────────────────────────────────
summary = pd.DataFrame({
    'Avg Slippage (bps)': slippage.mean().round(2),
    'Avg Spread Proxy (bps)': spread.mean().round(2),
    'Avg Market Impact (bps)': market_impact.mean().round(2),
    'Avg Implementation Shortfall (bps)': implementation_shortfall.mean().round(2),
    'IS Std Dev (bps)': implementation_shortfall.std().round(2)
})

summary.to_excel("reports/tca_summary_report.xlsx")
print("\n=== Final TCA Summary Report ===")
print(summary.to_string())
print("\nReport saved to reports/tca_summary_report.xlsx")