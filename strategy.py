import yfinance as yf
import pandas as pd

def compute_rsi(series: pd.Series, window: int) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/window, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/window, adjust=False).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def run_strategy(params):
    ticker     = params["ticker"]
    start      = params["start_date"]
    end        = params["end_date"]
    sma_period = params["sma_period"]
    rsi_period = params["rsi_period"]
    rsi_buy    = params["rsi_buy"]
    rsi_sell   = params["rsi_sell"]
    vol_period = params["vol_period"]

    # Download & flatten
    data = yf.download(ticker, start=start, end=end)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Indicators
    data["SMA"]       = data["Close"].rolling(window=sma_period).mean()
    data["RSI"]       = compute_rsi(data["Close"], window=rsi_period)
    data["VolumeAvg"] = data["Volume"].rolling(window=vol_period).mean()

    data.dropna(subset=["SMA", "RSI", "VolumeAvg"], inplace=True)

    # Signals
    data["Signal"] = "HOLD"
    buy_mask  = (data["Close"] > data["SMA"]) & (data["RSI"] < rsi_buy)
    sell_mask = (data["Close"] < data["SMA"]) & (data["RSI"] > rsi_sell)
    data.loc[buy_mask,  "Signal"] = "BUY"
    data.loc[sell_mask, "Signal"] = "SELL"

    # Calculate profit
    profit = 0.0
    entry_price = None
    for _, row in data.iterrows():
        if row.Signal == "BUY" and entry_price is None:
            entry_price = row.Close
        elif row.Signal == "SELL" and entry_price is not None:
            profit += row.Close - entry_price
            entry_price = None

    # Print summary
    print(f"Run complete — Profit: ${profit:.2f}")
    print(data[["Close", "SMA", "RSI", "Volume", "VolumeAvg", "Signal"]].tail(5))

    return data, profit
