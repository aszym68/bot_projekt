import json
import os
import talib
import config as cfg
import numpy as np
import pandas as pd
import yfinance as yf
from utils import get_repo_path
from datetime import datetime, timedelta
from symbols import corp_symbol

default_timedelta_days = 1825  # 5 lat


def download_data(symbol):
    if os.path.exists(get_repo_path() / cfg.CFG_FOLDER / cfg.CFG_JSON):
        with open(get_repo_path() / cfg.CFG_FOLDER / cfg.CFG_JSON, "r") as config_file:
            try:
                config = json.load(config_file)
                timedelta_days = config.get("timedelta_days", default_timedelta_days)
            except json.JSONDecodeError:
                print("Error reading config.json, using default timedelta.")
                timedelta_days = default_timedelta_days
    else:
        config = {"timedelta_days": default_timedelta_days}
        with open(get_repo_path() / cfg.CFG_FOLDER / cfg.CFG_JSON, "w") as config_file:
            json.dump(config, config_file, indent=4)
        timedelta_days = default_timedelta_days
    end_date = datetime.today()
    start_date = end_date - timedelta(timedelta_days)
    finance_data = yf.download(
        symbol,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d"),
        multi_level_index=False,
    )
    finance_data.to_csv(get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    config["last_download"] = end_date.strftime("%Y-%m-%d")
    with open(get_repo_path() / cfg.CFG_FOLDER / cfg.CFG_JSON, "w") as config_file:
        json.dump(config, config_file, indent=4)


def calculate_indicators(symbol):
    input_file = get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv"
    data = pd.read_csv(input_file)

    technical_indicators = {
        "SMA": "Simple Moving Average",
        "EMA": "Exponential Moving Average",
        "BBANDS": "Bollinger Bands",
        "ADX": "Average Directional Movement Index",
        "CCI": "Commodity Channel Index",
        "STOCH": "Stochastic Oscillator",
        "OBV": "On Balance Volume",
    }

    results = pd.DataFrame(index=data.index)
    results["SMA_20"] = talib.SMA(data["Close"], timeperiod=20)
    results["EMA_20"] = talib.EMA(data["Close"], timeperiod=20)

    upperband, middleband, lowerband = talib.BBANDS(
        data["Close"], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
    )
    results["BB_Upper"] = upperband
    results["BB_Middle"] = middleband
    results["BB_Lower"] = lowerband

    results["ADX_14"] = talib.ADX(
        data["High"], data["Low"], data["Close"], timeperiod=14
    )

    results["CCI_14"] = talib.CCI(
        data["High"], data["Low"], data["Close"], timeperiod=14
    )

    fastk, fastd = talib.STOCH(
        data["High"],
        data["Low"],
        data["Close"],
        fastk_period=14,
        slowk_period=3,
        slowk_matype=0,
        slowd_period=3,
        slowd_matype=0,
    )
    results["STOCH_K"] = fastk
    results["STOCH_D"] = fastd

    results["OBV"] = talib.OBV(data["Close"], data["Volume"])

    # fill NaN values with None to ensure compatibility
    results = results.where(pd.notnull(results), None)

    results.to_csv(get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}_tech.csv")


if __name__ == "__main__":
    for index, symbol in enumerate(corp_symbol.values()):
        print(f"Downloading data for {symbol}... ({index+1}/{len(corp_symbol)})")
        download_data(symbol)
        print(
            f"Calculating technical indicators for {symbol}... ({index+1}/{len(corp_symbol)})"
        )
        calculate_indicators(symbol)
        print("Done.")
