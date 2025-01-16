# TO DO:
# graph technical indicators (each one should have its own function!)


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io
from fetch_data import config as cfg
from fetch_data import symbols
from fetch_data import utils


def plot_stock_prices(symbol, days=90):
    if days <= 30:
        N = 5
    elif days <= 60:
        N = 10
    else:
        N = 15  # determine how many ticks to be shown
    main_df = pd.read_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    main_df.rename(
        columns={"Unnamed: 0": "Date"}, inplace=True
    )  # the date column's name gets lost for whatever reason
    colors = {
        "Close": "#8000ff",
        "High": "#00ff00",
        "Low": "#ff0000",
        "Open": "#ff00ff",
    }
    fig = plt.figure(figsize=(13, 8))
    ax = plt.subplot()
    for val in ["Close", "High", "Low", "Open"]:
        df = main_df.tail(days)[["Date", val]]
        ax.plot(df["Date"], df[val], "-o", markersize=0.5, color=colors[val], label=val)
    plt.xticks(df["Date"][::N], rotation=70)
    ax.legend()
    ax.set_title(symbol)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def plot_technical(symbol, days, indicator):
    indicator = symbols.technical_indicators[indicator]
    match indicator:
        case "SMA":
            return plotSMA(symbol, days)
        case "EMA":
            return plotEMA(symbol, days)
        case "BBANDS":
            return plotBB(symbol, days)
        case "ADX":
            return plotADX(symbol, days)
        case "CCI":
            return plotCCI(symbol, days)
        case "STOCH":
            return plotSTOCH(symbol, days)
        case "OBV":
            return plotOBV(symbol, days)
        case "RSI":
            return plotRSI(symbol, days)
        case "MACD":
            return plotMACD(symbol, days)
        case "ATR":
            return plotATR(symbol, days)
        case _:
            raise ValueError


def plotSMA(symbol, days=90):
    if days <= 30:
        N = 5
    elif days <= 60:
        N = 10
    else:
        N = 15
    df = pd.read_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    df = df.tail(days)
    plt.figure(figsize=(13, 8))
    plt.plot(df["Date"], df["SMA_14"], label="Simple Moving Average (SMA)", color="red")
    plt.xticks(df["Date"][::N], rotation=70)
    plt.xlabel("Date")
    plt.ylabel("SMA Value")
    plt.title(f"{symbol}, Simple Moving Average (14 days)")
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def plotEMA(symbol, days=90):
    if days <= 30:
        N = 5
    elif days <= 60:
        N = 10
    else:
        N = 15
    df = pd.read_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    df = df.tail(days)
    plt.figure(figsize=(13, 8))
    plt.plot(df["Date"], df["EMA_14"], label="Exponential Moving Average (SMA)")
    plt.xticks(df["Date"][::N], rotation=70)
    plt.xlabel("Date")
    plt.ylabel("EMA Value")
    plt.title(f"{symbol}, Exponential Moving Average (14 days)")
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def plotBB(symbol, days=90):
    if days <= 30:
        N = 5
    elif days <= 60:
        N = 10
    else:
        N = 15
    df = pd.read_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    df = df.tail(days)
    plt.figure(figsize=(13, 8))
    plt.plot(df["Date"], df["BB_Lower"], label="Lower Band", color="blue")
    plt.plot(df["Date"], df["BB_Upper"], label="Upper Band", color="orange")
    plt.plot(
        df["Date"], df["SMA_14"], "--", label="Simple Moving Average (SMA)", color="red"
    )
    plt.fill_between(
        df["Date"],
        df["BB_Lower"],
        df["BB_Upper"],
        where=(df["BB_Lower"] <= df["BB_Upper"]),
        color="lightcoral",
    )

    plt.legend()
    plt.title(f"{symbol}, Bollinger Bands (14 days)")
    plt.xticks(df["Date"][::N], rotation=70)
    plt.xlabel("Date")
    plt.ylabel("SMA Value")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def plotADX(symbol, days=90):
    if days <= 30:
        N = 5
    elif days <= 60:
        N = 10
    else:
        N = 15
    df = pd.read_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    df = df.tail(days)
    plt.figure(figsize=(13, 8))
    plt.plot(
        df["Date"],
        df["ADX_14"],
        label="Average Directional Movement Index (ADX)",
        color="red",
    )
    plt.xticks(df["Date"][::N], rotation=70)
    plt.xlabel("Date")
    plt.ylabel("ADX Value")
    plt.title(f"{symbol}, Average Directional Movement Index (14 days)")
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def plotCCI(symbol, days=90):
    if days <= 30:
        N = 5
    elif days <= 60:
        N = 10
    else:
        N = 15
    df = pd.read_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    df = df.tail(days)
    plt.figure(figsize=(13, 8))
    plt.plot(
        df["Date"],
        df["CCI_14"],
        label="Commodity Channel Index (CCI)",
        color="red",
    )
    plt.xticks(df["Date"][::N], rotation=70)
    plt.xlabel("Date")
    plt.ylabel("CCI Value")
    plt.title(f"{symbol}, Commodity Channel Index (14 days)")
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def plotSTOCH(symbol, days=90):
    if days <= 30:
        N = 5
    elif days <= 60:
        N = 10
    else:
        N = 15
    df = pd.read_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    df = df.tail(days)
    plt.figure(figsize=(13, 8))
    plt.plot(
        df["Date"],
        df["STOCH_K"],
        label="Stochastic %K",
        color="red",
    )
    plt.plot(
        df["Date"],
        df["STOCH_D"],
        label="Stochastic %D",
        color="blue",
    )
    plt.xticks(df["Date"][::N], rotation=70)
    plt.xlabel("Date")
    plt.ylabel("CCI Value")
    plt.title(f"{symbol}, Stochastic Oscillator (14 days)")
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def plotOBV(symbol, days=90):
    if days <= 30:
        N = 5
    elif days <= 60:
        N = 10
    else:
        N = 15
    df = pd.read_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    df = df.tail(days)
    plt.figure(figsize=(13, 8))
    plt.plot(df["Date"], df["OBV"], label="On-Balance Volume (OBV)", color="purple")
    plt.xticks(df["Date"][::N], rotation=70)
    plt.xlabel("Date")
    plt.ylabel("OBV Value")
    plt.title(f"{symbol}, On-Balance Volume")
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def plotRSI(symbol, days=90):
    if days <= 30:
        N = 5
    elif days <= 60:
        N = 10
    else:
        N = 15
    df = pd.read_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    df = df.tail(days)
    plt.figure(figsize=(13, 8))
    plt.plot(df["Date"], df["RSI_14"], label="RSI (14-day)")
    plt.axhline(70, color="red", linestyle="--", label="Overbought (70)")
    plt.axhline(30, color="blue", linestyle="--", label="Oversold (30)")
    plt.xticks(df["Date"][::N], rotation=70)
    plt.xlabel("Date")
    plt.ylabel("RSI")
    plt.title(f"{symbol}, Relative Strength Index")
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def plotMACD(symbol, days=90):
    if days <= 30:
        N = 5
    elif days <= 60:
        N = 10
    else:
        N = 15
    df = pd.read_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    df = df.tail(days)
    plt.figure(figsize=(13, 8))
    plt.plot(df["Date"], df["MACD"], label="MACD", color="blue")
    plt.plot(df["Date"], df["MACD_Signal"], label="Signal Line", color="red")
    plt.bar(
        df["Date"], df["MACD_Hist"], label="MACD Histogram", color="gray", alpha=0.6
    )
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
    plt.xticks(df["Date"][::N], rotation=70)
    plt.xlabel("Date")
    plt.ylabel("MACD Value")
    plt.title(f"{symbol}, MACD and Signal Line")
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


def plotATR(symbol, days=90):
    if days <= 30:
        N = 5
    elif days <= 60:
        N = 10
    else:
        N = 15
    df = pd.read_csv(utils.get_repo_path() / cfg.OUTPUT_PATH / f"{symbol}.csv")
    df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)
    plt.figure(figsize=(13, 8))
    plt.plot(df["Date"], df["ATR_14"], label="ATR (14-day)", color="green")
    plt.xticks(df["Date"][::N], rotation=70)
    plt.xlabel("Date")
    plt.ylabel("ATR Value")
    plt.title(f"{symbol}, Average True Range (Volatility)")
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf
