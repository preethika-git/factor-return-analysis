import pandas as pd
import yfinance as yf
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
from matplotlib import ticker as mtk

# INPUTS
stocks = [
    "ADANIENT.NS",  "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS",
    "AXISBANK.NS",  "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS",
    "BEL.NS",       "BHARTIARTL.NS", "BPCL.NS",       "BRITANNIA.NS",
    "CIPLA.NS",     "COALINDIA.NS",  "DIVISLAB.NS",   "DRREDDY.NS",
    "EICHERMOT.NS", "GRASIM.NS",     "HCLTECH.NS",    "HDFCBANK.NS",
    "HDFCLIFE.NS",  "HEROMOTOCO.NS", "HINDALCO.NS",   "HINDUNILVR.NS",
    "ICICIBANK.NS", "INDUSINDBK.NS", "INFY.NS",       "ITC.NS",
    "JIOFIN.NS",    "JSWSTEEL.NS",   "KOTAKBANK.NS",  "LT.NS",
    "M&M.NS",       "MARUTI.NS",     "NESTLEIND.NS",  "NTPC.NS",
    "ONGC.NS",      "POWERGRID.NS",  "RELIANCE.NS",   "SBILIFE.NS",
    "SBIN.NS",      "SHRIRAMFIN.NS", "SUNPHARMA.NS",  "TATACONSUM.NS",
    "TATASTEEL.NS", "TCS.NS",        "TECHM.NS",
    "TITAN.NS",     "ULTRACEMCO.NS"
]

end = pd.to_datetime(date.today()) - pd.offsets.MonthEnd(1)
start = end - pd.DateOffset(years=1)
mom_start = end - pd.DateOffset(years=2)

price = yf.download(tickers=stocks, start=mom_start, end=end)["Close"]

# Fetch all ticker info in one pass
ticker_info = {stock: yf.Ticker(stock).info for stock in price.columns}

# Define Returns
def short_return(df):
    return np.average(df["Return"][df["Positions"]=="Short"])
def long_return(df):
    return np.average(df["Return"][df["Positions"]=="Long"])
def portfolio_return(df):
    return np.average(df["Return"])

# Size Portfolio - Create and Calculate Returns
mcap = pd.DataFrame({
    stock: price[stock][price.index <= start].iloc[-1] * ticker_info[stock]["sharesOutstanding"]
    for stock in price.columns
}, index=["mcap"]).T
mcap["rank"] = mcap["mcap"].rank()

size_stk = {}
for i in range(len(mcap)):
    if mcap.iloc[i,1] <= 10:
        size_stk[mcap.index[i]] = "Long"
    elif mcap.iloc[i,1] > len(mcap) - 10:
        size_stk[mcap.index[i]] = "Short"
    else:
        continue

size_p = pd.DataFrame(size_stk, index=["Positions"]).T
size_p = size_p.sort_values("Positions")
size_p = size_p.reset_index()
size_p.rename(columns={"index": "Stock"}, inplace=True)

size_p[f"Price as on: {start.date()}"] = size_p["Stock"].map(price.asof(start))
size_p[f"Price as on: {end.date()}"] = size_p["Stock"].map(price.asof(pd.to_datetime(end)))

for i in range(len(size_p)):
    if size_p.loc[i,"Positions"] == "Long":
        size_p.loc[i,"Return"] = size_p.loc[i,f"Price as on: {end.date()}"] / size_p.loc[i,f"Price as on: {start.date()}"] - 1
    elif size_p.loc[i,"Positions"] == "Short":
        size_p.loc[i,"Return"] = 1 - size_p.loc[i,f"Price as on: {end.date()}"] / size_p.loc[i,f"Price as on: {start.date()}"]

size_short_return = short_return(size_p)
size_long_return = long_return(size_p)
size_portfolio_return = portfolio_return(size_p)

# Value Portfolio - Create and Calculate Returns
pb = pd.DataFrame({
    stock: price[stock][price.index <= start].iloc[-1] / ticker_info[stock]["bookValue"]
    for stock in price.columns
}, index=["p/b"]).T
pb["rank"] = pb["p/b"].rank()

value_stk = {}
for i in range(len(pb)):
    if pb.iloc[i,1] <= 10:
        value_stk[pb.index[i]] = "Long"
    elif pb.iloc[i,1] > len(pb) - 10:
        value_stk[pb.index[i]] = "Short"
    else:
        continue

value_p = pd.DataFrame(value_stk, index=["Positions"]).T
value_p = value_p.sort_values("Positions")
value_p = value_p.reset_index()
value_p.rename(columns={"index": "Stock"}, inplace=True)

value_p[f"Price as on: {start.date()}"] = value_p["Stock"].map(price.asof(start))
value_p[f"Price as on: {end.date()}"] = value_p["Stock"].map(price.asof(pd.to_datetime(end)))

for i in range(len(value_p)):
    if value_p.loc[i,"Positions"] == "Long":
        value_p.loc[i,"Return"] = value_p.loc[i,f"Price as on: {end.date()}"] / value_p.loc[i,f"Price as on: {start.date()}"] - 1
    elif value_p.loc[i,"Positions"] == "Short":
        value_p.loc[i,"Return"] = 1 - value_p.loc[i,f"Price as on: {end.date()}"] / value_p.loc[i,f"Price as on: {start.date()}"]

value_short_return = short_return(value_p)
value_long_return = long_return(value_p)
value_portfolio_return = portfolio_return(value_p)

# Momentum Portfolio - Create and Calculate Returns
mom = pd.DataFrame({
    stock: price[stock][price.index >= start].iloc[0] / price[stock][price.index >= mom_start].iloc[0] - 1
    for stock in price.columns
}, index=["mom_score"]).T
mom["rank"] = mom["mom_score"].rank(ascending=False)

mom_stk = {}
for i in range(len(mom)):
    if mom.iloc[i,1] <= 10:
        mom_stk[mom.index[i]] = "Long"
    elif mom.iloc[i,1] > len(mom) - 10:
        mom_stk[mom.index[i]] = "Short"
    else:
        continue

mom_p = pd.DataFrame(mom_stk, index=["Positions"]).T
mom_p = mom_p.sort_values("Positions")
mom_p = mom_p.reset_index()
mom_p.rename(columns={"index": "Stock"}, inplace=True)

mom_p[f"Price as on: {start.date()}"] = mom_p["Stock"].map(price.asof(start))
mom_p[f"Price as on: {end.date()}"] = mom_p["Stock"].map(price.asof(pd.to_datetime(end)))

for i in range(len(mom_p)):
    if mom_p.loc[i,"Positions"] == "Long":
        mom_p.loc[i,"Return"] = mom_p.loc[i,f"Price as on: {end.date()}"] / mom_p.loc[i,f"Price as on: {start.date()}"] - 1
    elif mom_p.loc[i,"Positions"] == "Short":
        mom_p.loc[i,"Return"] = 1 - mom_p.loc[i,f"Price as on: {end.date()}"] / mom_p.loc[i,f"Price as on: {start.date()}"]

mom_short_return = short_return(mom_p)
mom_long_return = long_return(mom_p)
mom_portfolio_return = portfolio_return(mom_p)

# Create Monthly Returns DF
monthly_price = price.resample("ME").last()
monthly_returns = monthly_price[start:end].pct_change()

# Define and Calculate Monthly Returns and Cummulative Returns for each Portfolio
def ret_cumRet(m_ret, p):
    m_ret["return"] = monthly_returns[p["Stock"][p["Positions"]=="Long"]].mean(axis=1) - monthly_returns[p["Stock"][p["Positions"]=="Short"]].mean(axis=1)
    m_ret = m_ret.dropna(subset=["return"]).copy()
    m_ret["cum_return"] = (1 + m_ret["return"]).cumprod() - 1
    return m_ret

size_m_ret = pd.DataFrame({stock: monthly_returns[stock] for stock in size_stk.keys()}, index=monthly_returns.index, columns=size_stk.keys())
size_m_ret = ret_cumRet(size_m_ret, size_p)

value_m_ret = pd.DataFrame({stock: monthly_returns[stock] for stock in value_stk.keys()}, index=monthly_returns.index, columns=value_stk.keys())
value_m_ret = ret_cumRet(value_m_ret, value_p)

mom_m_ret = pd.DataFrame({stock: monthly_returns[stock] for stock in mom_stk.keys()}, index=monthly_returns.index, columns=mom_stk.keys())
mom_m_ret = ret_cumRet(mom_m_ret, mom_p)

# Sharpe Ratio Formula
def sharpe_ratio(portfolio_return, risk_free, m_returns):
    sharpe = (portfolio_return - risk_free) / (np.std(m_returns) * np.sqrt(12))
    return sharpe

r_f = .069

#Calculate Sharpe Ratios for each Portfolio
size_sharpe = sharpe_ratio(risk_free=r_f, portfolio_return=size_portfolio_return, m_returns=size_m_ret["return"])
value_sharpe = sharpe_ratio(risk_free=r_f, portfolio_return=value_portfolio_return, m_returns=value_m_ret["return"])
mom_sharpe = sharpe_ratio(risk_free=r_f, portfolio_return=mom_portfolio_return, m_returns=mom_m_ret["return"])

sharpe_ratios = pd.DataFrame({
    "Size":  [size_sharpe,  size_portfolio_return,  size_long_return,  size_short_return],
    "Value": [value_sharpe, value_portfolio_return, value_long_return, value_short_return],
    "Momentum": [mom_sharpe, mom_portfolio_return,  mom_long_return,   mom_short_return]
}, index=["Sharpe Ratio", "Portfolio Return", "Long Return", "Short Return"]).T

# Chart inputs
mom_y = mom_m_ret["cum_return"]
value_y = value_m_ret["cum_return"]
size_y = size_m_ret["cum_return"]

maxmom = max(mom_m_ret["cum_return"])
maxval = max(value_m_ret["cum_return"])
maxsize = max(size_m_ret["cum_return"])

minmom = min(mom_m_ret["cum_return"])
minval = min(value_m_ret["cum_return"])
minsize = min(size_m_ret["cum_return"])

# Charts Plotting and Formatting
fig, ax = plt.subplots(figsize=(11,6))

fmt = dict(marker="o", markersize=3, mfc="k", lw=1)

ax.plot(size_m_ret.index, size_y, label="Size", color="blue", **fmt)
ax.plot(value_m_ret.index, value_y, label="Value", color="red", **fmt)
ax.plot(mom_m_ret.index, mom_y, label="Momentum", color="green", **fmt)

ax.set_xticks(size_m_ret.index)
ax.set_xticklabels([d.strftime("%b-%Y") for d in size_m_ret.index], rotation=45)
ax.set_xlim(mom_m_ret.index[0] - pd.DateOffset(days=10), mom_m_ret.index[-1] + pd.DateOffset(days=10))

ax.yaxis.set_major_formatter(mtk.PercentFormatter(xmax=1.0))
ax.set_ylim(min(minmom,minsize,minval)-0.05, max(maxmom,maxsize,maxval)+0.05)

ax.axhline(0, lw=.7, ls="-", color="grey")
ax.legend(loc="best")

ax.set_title("Cumulative Monthly Returns of Factor Portfolios")
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Return")

plt.tight_layout()

# Exporting Results and Charts
import os
os.makedirs("output", exist_ok=True)

fig.savefig("output/factor_returns.png", dpi=150, bbox_inches="tight")

with pd.ExcelWriter("output/factor_portfolio.xlsx", engine = "xlsxwriter") as writer:
    sharpe_ratios.to_excel(writer, sheet_name="sharpe_ratios")    
    size_p.to_excel(writer, index=False, sheet_name="size_portfolio")
    value_p.to_excel(writer, index=False, sheet_name="value_portfolio")
    mom_p.to_excel(writer, index=False, sheet_name="momentum_portfolio")