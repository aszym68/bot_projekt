import json
import os
import talib
import numpy as np
import pandas as pd
import yfinance as yf
from fetch_data import config as cfg
from datetime import datetime, timedelta
from fetch_data import symbols
from fetch_data import utils

default_timedelta_days = 1825  # 5 lat


def download_data(symbol):
    if os.path.exists(utils.get_repo_path() / cfg.CFG_FOLDER / cfg.CFG_JSON):
        with open(
            utils.get_repo_path() / cfg.CFG_FOLDER / cfg.CFG_JSON, "r"
        ) as config_file:
            try:
                config = json.load(config_file)
                timedelta_days = config.get("timedelta_days", default_timedelta_days)
            except json.JSONDecodeError:
                print("Error reading config.json, using default timedelta.")
                timedelta_days = default_timedelta_days
    else:
        config = {"timedelta_days": default_timedelta_days}
        with open(
            utils.get_repo_path() / cfg.CFG_FOLDER / cfg.CFG_JSON, "w"
        ) as config_file:
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
    finance_data.index = pd.to_datetime(finance_data.index).date
    finance_data.to_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    config["last_download"] = end_date.strftime("%Y-%m-%d")
    with open(
        utils.get_repo_path() / cfg.CFG_FOLDER / cfg.CFG_JSON, "w"
    ) as config_file:
        json.dump(config, config_file, indent=4)


def calculate_indicators(symbol):
    input_file = utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv"
    data = pd.read_csv(input_file)

    technical_indicators = {
        "SMA": "Simple Moving Average",
        "EMA": "Exponential Moving Average",
        "BBANDS": "Bollinger Bands",
        "ADX": "Average Directional Movement Index",
        "CCI": "Commodity Channel Index",
        "STOCH": "Stochastic Oscillator",
        "OBV": "On Balance Volume",
        "RSI": "Relative Strength Index",
        "MACD": "Moving Average Convergence Divergence",
        "ATR": "Average True Range",
    }

    data["SMA_14"] = talib.SMA(data["Close"], timeperiod=14)
    data["EMA_14"] = talib.EMA(data["Close"], timeperiod=14)

    upperband, middleband, lowerband = talib.BBANDS(
        data["Close"], timeperiod=14, nbdevup=2, nbdevdn=2, matype=0
    )
    data["BB_Upper"] = upperband
    data["BB_Middle"] = middleband
    data["BB_Lower"] = lowerband

    data["ADX_14"] = talib.ADX(data["High"], data["Low"], data["Close"], timeperiod=14)

    data["CCI_14"] = talib.CCI(data["High"], data["Low"], data["Close"], timeperiod=14)

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
    data["STOCH_K"] = fastk
    data["STOCH_D"] = fastd

    data["OBV"] = talib.OBV(data["Close"], data["Volume"])

    data["RSI_14"] = talib.RSI(data["Close"], timeperiod=14)
    data["MACD"], data["MACD_Signal"], data["MACD_Hist"] = talib.MACD(
        data["Close"], fastperiod=12, slowperiod=26, signalperiod=9
    )
    data["ATR_14"] = talib.ATR(data["High"], data["Low"], data["Close"], timeperiod=14)

    # fill NaN values with None to ensure compatibility
    data = data.where(pd.notnull(data), None)

    data.to_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")


def main():
    for index, symbol in enumerate(symbols.corp_symbol.values()):
        print(
            f"Downloading data for {symbol}... ({index+1}/{len(symbols.corp_symbol)})"
        )
        download_data(symbol)
        print(
            f"Calculating technical indicators for {symbol}... ({index+1}/{len(symbols.corp_symbol)})"
        )
        calculate_indicators(symbol)
        print("Done.")


if __name__ == "__main__":
    main()
