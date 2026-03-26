# Nifty 50 Factor Investing Backtest

A long-short factor backtest on Nifty 50 stocks across three classic factors: **momentum**, **value**, and **size**, over a rolling 12-month window ending today.

## What This Project Does

For each of the three factors, the project:

1. **Ranks** all Nifty 50 stocks on that factor using today's fundamental data
2. **Splits** stocks into a top group (long leg) and bottom group (short leg)
3. **Constructs** an equal-weighted long-short portfolio
4. **Tracks** daily returns of that portfolio over the past 12 months
5. **Reports** a cumulative return chart and Sharpe ratio for each factor

Run it any day and it automatically evaluates the most recent 12-month window.

## Factors 

Momentum: 12-month trailing return ending today 
Value: P/B ratio (book value per share ÷ price on start date) 
Size: Market cap (shares outstanding × price on start date) 

## Universe

Nifty 50 constituents (Yahoo Finance tickers, `.NS` suffix for NSE).  
**Note:** `TATAMOTORS.NS` was delisted following the Oct 2025 demerger. Use `TMPV.NS` (passenger vehicles) and/or `TMCV.NS` (commercial vehicles) as replacements. Due to inconsistencies in data availability with this particular stock, I've removed it from the universe 

## Data Approach

All fundamental data (shares outstanding, book value per share) is sourced from `yfinance` at runtime and reflects the most recently reported figures. Price data is pulled historically for the trailing 12-month window.

- **Market cap** = shares outstanding (latest reported) × price on start date (12 months ago)
- **P/B** = book value per share (latest reported) ÷ price on start date
- **Momentum** = total return from 12 months ago to today

The ranking snapshot and the performance window both anchor to the same start date, so there is no look-ahead bias. The minor approximation is that shares outstanding and book value reflect today's reported figures rather than exactly what they were 12 months ago.

## Output

Three charts, one per factor:
- X-axis: daily dates over the trailing 12-month window
- Y-axis: cumulative return of the long-short portfolio (rebased to 0)
- Annotation: annualised Sharpe ratio (assuming risk-free rate = 6.5% p.a.)

## Key Assumptions

- **Rebalancing:** Single rebalance at the start of each 12-month window (no intra-period rebalancing)
- **Weighting:** Equal weight within each leg
- **Costs:** No transaction costs or slippage modelled
- **Data source:** `yfinance` for both price history and fundamentals
- **Risk-free rate:** 6.5% p.a. for Sharpe ratio calculation