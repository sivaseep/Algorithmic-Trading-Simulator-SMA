import yfinance as yf
import pandas as pd 
import matplotlib.pyplot as plt 

#download stock data
data = yf.download("AAPL", start = "2020-01-01", end = "2024-01-01")

#calculate moving averages

data["SMA_20"] = data["Close"].rolling(window=20).mean()
data["SMA_50"] = data["Close"].rolling(window=50).mean()

#create trading signals

data["Signal"] = 0
data.loc[data["SMA_20"] > data["SMA_50"], "Signal"] = 1
data["Position"] = data["Signal"].shift(1)

#calculate returns

data["Market_Return"] = data["Close"].pct_change(1)
data["Strategy_Return"] = data["Position"] * data["Market_Return"]

#calculate cumulative performance

data["Market_Cumulative"] = (1 + data["Market_Return"]).cumprod()
data["Strategy_Cumulative"] = (1 + data["Strategy_Return"]).cumprod()

#plot results

plt.figure(figsize=(12, 6))
plt.plot(data["Market_Cumulative"], label = "Buy and Hold")
plt.plot(data["Strategy_Cumulative"], label = "Strategy")
plt.title("Trading Strategy vs Buy and Hold")
plt.legend()
plt.show()
