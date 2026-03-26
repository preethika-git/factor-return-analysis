import pandas as pd
import yfinance as yf
import numpy as np
from datetime import date

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
    "TATASTEEL.NS",  "TCS.NS",        "TECHM.NS",
    "TITAN.NS",     "ULTRACEMCO.NS"
]

end = date.today()
start = end - pd.DateOffset(years=1)
mom_start = end - pd.DateOffset(years=2)

price = yf.download(tickers=stocks, start=mom_start, end=end)["Close"]

mcap = pd.DataFrame({
    stock : price[stock].loc[start] * yf.Ticker(stock).info["sharesOutstanding"]
    for stock in price.columns
},index=["mcap"]).T
mcap["rank"] = mcap["mcap"].rank()

size_stk = {}
for i in range(len(mcap)):
    if mcap.iloc[i,1] <= 10:
        size_stk[mcap.index[i]] = "Long"
    elif mcap.iloc[i,1] > len(mcap) - 10:
        size_stk[mcap.index[i]] ="Short"
    else:
        continue

size_p = pd.DataFrame(size_stk, index=["Positions"]).T
size_p = size_p.sort_values("Positions")
size_p = size_p.reset_index()
size_p.rename(columns = {"index":"Stock"}, inplace = True)

size_p[f"Price as on: {start.date()}"] = size_p["Stock"].map(price.asof(start))
size_p[f"Price as on: {end}"] = size_p["Stock"].map(price.asof(pd.to_datetime(end)))

for i in range(len(size_p)):
    if size_p.loc[i,"Positions"] == "Long":
        size_p.loc[i,"Return"] = size_p.loc[i,f"Price as on: {end}"] / size_p.loc[i,f"Price as on: {start.date()}"] - 1
    elif size_p.loc[i,"Positions"] == "Short":
        size_p.loc[i,"Return"] = 1- size_p.loc[i,f"Price as on: {end}"] / size_p.loc[i,f"Price as on: {start.date()}"]
    else:
        continue

size_short_return = np.average(size_p["Return"][size_p["Positions"]=="Short"])
size_long_return = np.average(size_p["Return"][size_p["Positions"]=="Long"])
size_portfolio_return = np.average(size_p["Return"])

pb = pd.DataFrame({
    stock : price[stock].loc[start] / yf.Ticker(stock).info["bookValue"]
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
value_p.rename(columns = {"index":"Stock"}, inplace = True)

value_p[f"Price as on: {start.date()}"] = value_p["Stock"].map(price.asof(start))
value_p[f"Price as on: {end}"] = value_p["Stock"].map(price.asof(pd.to_datetime(end)))

for i in range(len(value_p)):
    if value_p.loc[i,"Positions"] == "Long":
        value_p.loc[i,"Return"] = value_p.loc[i,f"Price as on: {end}"] / value_p.loc[i,f"Price as on: {start.date()}"] - 1
    elif value_p.loc[i,"Positions"] == "Short":
        value_p.loc[i,"Return"] = 1- value_p.loc[i,f"Price as on: {end}"] / value_p.loc[i,f"Price as on: {start.date()}"]
    else:
        continue

value_short_return = np.average(value_p["Return"][value_p["Positions"]=="Short"])
value_long_return = np.average(value_p["Return"][value_p["Positions"]=="Long"])
value_portfolio_return = np.average(value_p["Return"])

mom = pd.DataFrame({
    stock: price.loc[mom_start,stock] / price.loc[start,stock] -1
    for stock in price.columns
}, index = ["mom_score"]).T
mom["rank"] = mom["mom_score"].rank(ascending = False)

mom_stk = {}
for i in range(len(mom)):
    if mom.iloc[i,1] <= 10:
        mom_stk[mom.index[i]] = "Long"
    elif mom.iloc[i,1] > len(pb) - 10:
        mom_stk[mom.index[i]] = "Short"
    else:
        continue

mom_p = pd.DataFrame(mom_stk, index=["Positions"]).T
mom_p = mom_p.sort_values("Positions")
mom_p = mom_p.reset_index()
mom_p.rename(columns = {"index":"Stock"}, inplace = True)

mom_p[f"Price as on: {start.date()}"] = mom_p["Stock"].map(price.asof(start))
mom_p[f"Price as on: {end}"] = mom_p["Stock"].map(price.asof(pd.to_datetime(end)))

for i in range(len(mom_p)):
    if mom_p.loc[i,"Positions"] == "Long":
        mom_p.loc[i,"Return"] = mom_p.loc[i,f"Price as on: {end}"] / mom_p.loc[i,f"Price as on: {start.date()}"] - 1
    elif mom_p.loc[i,"Positions"] == "Short":
        mom_p.loc[i,"Return"] = 1- mom_p.loc[i,f"Price as on: {end}"] / mom_p.loc[i,f"Price as on: {start.date()}"]
    else:
        continue

mom_short_return = np.average(mom_p["Return"][mom_p["Positions"]=="Short"])
mom_long_return = np.average(mom_p["Return"][mom_p["Positions"]=="Long"])
mom_portfolio_return = np.average(mom_p["Return"])