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
    match indicator:
        case "SMA":
            plotSMA(symbol, days)
        case "EMA":
            plotEMA(symbol, days)
        case "BB":
            plotBB(symbol, days)
        case "ADX":
            plotADX(symbol, days)
        case "CCI":
            plotCCI(symbol, days)
        case "STOCH":
            plotSTOCH(symbol, days)
        case "OBV":
            plotOBV(symbol, days)


def plotSMA(symbol, days=90):
    pass


def plotEMA(symbol, days=90):
    pass


def plotBB(symbol, days=90):
    pass


def plotADX(symbol, days=90):
    pass


def plotCCI(symbol, days=90):
    pass


def plotSTOCH(symbol, days=90):
    pass


def plotOBV(symbol, days=90):
    pass
