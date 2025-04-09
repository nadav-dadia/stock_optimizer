import json
import os
import subprocess
import pandas as pd
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK

# Paths
BASE_DIR     = os.path.dirname(__file__)
PARAMS_FP    = os.path.join(BASE_DIR, "params.json")
LOG_FP       = os.path.join(BASE_DIR, "iteration_log.csv")
BACKTEST_CMD = ["python", os.path.join(BASE_DIR, "run_backtest.py")]

# Search space for only the dynamic fields
space = {
    "sma_period": hp.quniform("sma_period", 5, 300, 5),
    "rsi_buy":    hp.quniform("rsi_buy",    10, 90, 5),
    "rsi_sell":   hp.quniform("rsi_sell",   10, 90, 5),
    "vol_period": hp.quniform("vol_period", 5, 100, 5),
}

def load_all_params():
    with open(PARAMS_FP, "r") as f:
        return json.load(f)

def save_all_params(params):
    with open(PARAMS_FP, "w") as f:
        json.dump(params, f, indent=4)

def objective(dynamic_params):
    # Load static fields
    all_params = load_all_params()
    # Merge dynamic (casting to int)
    for k, v in dynamic_params.items():
        all_params[k] = int(v)

    # Save merged params
    save_all_params(all_params)

    # Run backtest silently
    subprocess.run(BACKTEST_CMD, check=True, stdout=subprocess.DEVNULL)

    # Read profit
    log_df = pd.read_csv(LOG_FP)
    profit = log_df.iloc[-1].profit

    # Minimize negative profit
    return {"loss": -profit, "status": STATUS_OK}

def main(max_evals=30):
    trials = Trials()
    best = fmin(
        fn=objective,
        space=space,
        algo=tpe.suggest,
        max_evals=max_evals,
        trials=trials
    )

    # Merge best back into full params
    all_params = load_all_params()
    for k, v in best.items():
        all_params[k] = int(v)

    print("\n=== Best parameters found ===")
    print(json.dumps(all_params, indent=2))
    save_all_params(all_params)

if __name__ == "__main__":
    main()
