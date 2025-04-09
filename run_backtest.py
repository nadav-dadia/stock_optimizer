import json
import os
import pandas as pd
from strategy import run_strategy
from datetime import datetime

# Paths
base_dir   = os.path.dirname(__file__)
params_fp  = os.path.join(base_dir, "params.json")
log_fp     = os.path.join(base_dir, "iteration_log.csv")

# Load params
with open(params_fp, "r") as f:
    params = json.load(f)

# Run strategy
df, profit = run_strategy(params)

# Metrics
total = len(df)
buys  = (df.Signal == "BUY").sum()
sells = (df.Signal == "SELL").sum()

# Log entry
entry = {
    "run_id":        datetime.now().strftime("%Y%m%d_%H%M%S"),
    "date":          datetime.now().strftime("%Y-%m-%d"),
    "sma_period":    params["sma_period"],
    "rsi_period":    params["rsi_period"],
    "vol_period":    params["vol_period"],
    "total_signals": total,
    "buy_signals":   buys,
    "sell_signals":  sells,
    "profit":        round(profit, 2)
}

# Append to CSV
df_log = pd.DataFrame([entry])
if not os.path.exists(log_fp):
    df_log.to_csv(log_fp, index=False)
else:
    df_log.to_csv(log_fp, mode="a", header=False, index=False)

print(f"Logged iteration to {log_fp}")
