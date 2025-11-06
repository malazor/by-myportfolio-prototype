import pandas as pd
import numpy as np

def generate_stats(prices):
    output={}
    df = pd.DataFrame(prices)
    df["date"] = pd.to_datetime(df["date"])
    df["close"] = pd.to_numeric(df["close"])
    df["volume"] = pd.to_numeric(df["volume"])
    # df = df.set_index("date").sort_index()

#    df.set_index("date", inplace=True)

    first_close = df["close"].iloc[0]   # primer valor de la serie
    last_close  = df["close"].iloc[-1]  # último valor de la serie

    return_pct_simple = (last_close / first_close - 1) * 100
    return_pct_log = np.log(last_close / first_close) * 100

    min_row = df.loc[df["close"].idxmin(), ["date", "close"]]
    max_row = df.loc[df["close"].idxmax(), ["date", "close"]]

    volume_total = df["volume"].sum()
    volume_mean  = df["volume"].mean()
    volume_median = df["volume"].median()

    output["count_days"]= len(df)
    output["first_date"]= df["date"].min()
    output["last_date"]= df["date"].max()
    output["min_price"]= df["close"].min()
    output["max_price"]= df["close"].max()
    output["mean_price"]= df["close"].mean()
    output["std_price"]= df["close"].std()
    output["return_pct_simple"] = return_pct_simple
    output["return_pct_log"] = return_pct_log
    output["high_low_extremes"] = {
    "max_high": max_row.to_dict(),
    "min_low": min_row.to_dict()
    }
    output["volume"] = {
       "total": int(volume_total),
       "mean": int(volume_mean),
       "median": int(volume_median)
    }




    return output

def calculate_market_value(data: list[dict]) -> float:
    total_cantidad = sum(item["cantidad"] for item in data)
    if total_cantidad == 0:
        return 0.0
    return sum((item["cantidad"] / total_cantidad) * item["precio_compra"] for item in data)

def calculate_ratio_sharpe(input) -> float:
    output = 0
    try:
        # df = pd.DataFrame(input)
        # print(df)      
        pass
    except Exception as e:
        print(e)

    return output

def calculate_volatility(input: dict) -> float:
    output = 0
    return output
