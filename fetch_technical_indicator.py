import requests
import pandas as pd
from symbols import corp_symbol

# Lista wskaźników technicznych dostępnych w Alpha Vantage
technical_indicators = {
    "SMA": "Simple Moving Average",  # Prosta średnia krocząca
    "EMA": "Exponential Moving Average",  # Wykładnicza średnia krocząca
    "MACD": "Moving Average Convergence Divergence",  # Zbieżność i rozbieżność średnich ruchomych
    "RSI": "Relative Strength Index",  # Wskaźnik siły relatywnej
    "BBANDS": "Bollinger Bands",  # Wstęgi Bollingera
    "ATR": "Average True Range",  # Średnia zmienność
    "ADX": "Average Directional Movement Index",  # Średni wskaźnik kierunkowy
    "CCI": "Commodity Channel Index",  # Wskaźnik kanału towarowego
    "STOCH": "Stochastic Oscillator",  # Oscylator stochastyczny
    "WILLR": "Williams %R",  # Williams Percent Range
    "ROC": "Rate of Change",  # Wskaźnik tempa zmiany
    "MFI": "Money Flow Index",  # Indeks przepływów pieniężnych
    "OBV": "On Balance Volume",  # Objętość bilansowa
    "TRIX": "Triple Exponential Average",  # Potrójna średnia wykładnicza
    "VWAP": "Volume Weighted Average Price",  # Średnia ważona wolumenem
    "AD": "Accumulation/Distribution Line",  # Linia akumulacji/dystrybucji
    "ADX": "Average Directional Movement Index"  # Indeks średniego ruchu kierunkowego
}


def fetch_technical_indicator(company_name, indicator, interval='daily', time_period=14, series_type='close',
                              api_key='HRVCBXNVYPUS72OM'):
    """
    Pobiera wskaźnik techniczny z API Alpha Vantage.

    :param company_name: Nazwa korporacji (np. 'Apple', 'Microsoft')
    :param indicator: Typ wskaźnika (np. 'RSI', 'SMA', 'EMA', 'MACD').
    :param interval: Interwał danych (np. 'daily', '5min', '1min').
    :param time_period: Okres obliczeniowy wskaźnika (np. 14 dla RSI).
    :param series_type: Typ ceny (np. 'close', 'open', 'high', 'low').
    :param api_key: Klucz API Alpha Vantage.
    :return: DataFrame z wynikami wskaźnika lub None w przypadku błędu.
    """

    if company_name not in corp_symbol:
        print(f"Błąd: {company_name} nie znajduje się na liście obsługiwanych korporacji.")
        return None

    symbol = corp_symbol[company_name]

    url = f"https://www.alphavantage.co/query?function={indicator}&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Wybierz odpowiedni klucz w zależności od wskaźnika (np. 'Technical Analysis: RSI')
        key = f"Technical Analysis: {indicator.upper()}"
        if key in data:
            df = pd.DataFrame.from_dict(data[key], orient='index').reset_index()
            df.rename(columns={'index': 'timestamp'}, inplace=True)
            return df
        else:
            print("Brak danych dla podanego wskaźnika.")
            return None
    else:
        print(f"Nie udało się pobrać danych. Kod statusu: {response.status_code}")
        return None
