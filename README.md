# Nifty 50 Factor Investing Backtest

A long-short factor backtest on Nifty 50 stocks across three classic factors: **momentum**, **value** and **size**, over a rolling 12-month window ending today.


## What This Project Does

For each of the three factors, the project:

1. Ranks all Nifty 50 stocks on that factor using today's fundamental data
2. Splits stocks into a top group (long leg) and bottom group (short leg)
3. Constructs an equal-weighted long-short portfolio
4. Tracks monthly returns of that portfolio over the past 12 months
5. Reports a cumulative return chart, Sharpe ratio, Alpha and Beta for each factor

Run it any day and it automatically evaluates the most recent 12-month window.


## Factors

| Factor | Metric | Long leg | Short leg |
|--------|--------|----------|-----------|
| Momentum | 12-month trailing return ending at start date | Top 10 by return | Bottom 10 by return |
| Value | P/B ratio (price ÷ book value per share) at start date | Bottom 10 by P/B (cheapest) | Top 10 by P/B (most expensive) |
| Size | Market cap (shares outstanding × price at start date) | Bottom 10 by market cap (small) | Top 10 by market cap (large) |


## Universe

Nifty 50 constituents (Yahoo Finance tickers, `.NS` suffix for NSE).  
**Note:** `TATAMOTORS.NS` was delisted following the Oct 2025 demerger. Replaced with `TMPV.NS` (passenger vehicles) and `TMCV.NS` (commercial vehicles).


## Data Approach

All fundamental data (shares outstanding, book value per share) is sourced from `yfinance` at runtime in a single pass and reflects the most recently reported figures. Price data is pulled historically for the trailing 24-month window (12 months for momentum ranking + 12 months for performance tracking).

- **Market cap** = shares outstanding × price on start date
- **P/B** = price on start date ÷ book value per share (latest reported)
- **Momentum score** = return from 24 months ago to 12 months ago

The ranking snapshot and the performance window both anchor to the same start date, so there is no look-ahead bias. The minor approximation is that shares outstanding and book value reflect today's reported figures rather than exactly what they were 12 months ago.


## Output

All outputs are saved to the `output/` folder:

- `factor_returns.png` — cumulative monthly return chart for all three factor portfolios
- `factor_portfolio.xlsx` — Excel workbook with the following sheets:
  - `sharpe_ratios` — annualised Sharpe ratio, portfolio return, long return, and short return for each factor
  - `alpha_beta` — annualised Alpha and Beta for each factor
  - `size_portfolio` — stock-level positions and returns for the size factor
  - `value_portfolio` — stock-level positions and returns for the value factor
  - `momentum_portfolio` — stock-level positions and returns for the momentum factor


## Project Structure

```
factor-return-analysis/
├── factor_return.py
├── README.md
├── requirements.txt
├── .gitignore
└── output/             # generated on run, gitignored
    ├── factor_returns.png
    └── factor_portfolio.xlsx
```


## Key Assumptions

- **Rebalancing:** Single rebalance at the start of each 12-month window (no intra-period rebalancing)
- **Weighting:** Equal weight within each leg
- **Costs:** No transaction costs or slippage modelled
- **Data source:** `yfinance` for both price history and fundamentals
- **Risk-free rate:** 6.9% p.a. for Sharpe ratio calculation
- **Sharpe ratio:** Annualised using monthly standard deviation × √12
- **CAPM regression:** Alpha and beta estimated via OLS regression of monthly portfolio returns against Nifty 50 (^NSEI) monthly returns. Alpha is annualised using (1 + α)^12 - 1


## Setup

```bash
pip install -r requirements.txt
python factor_return.py
```