import requests
import pandas as pd
from io import StringIO

corp_symbol = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Amazon': 'AMZN',
    'Alphabet': 'GOOG',
    'Tesla': 'TSLA',
    'Nvidia': 'NVDA',
    'Meta Platforms': 'META'
}


def fetch_stock_data(company_name, api_key='HRVCBXNVYPUS72OM', interval='5min'):
    """
    Pobiera dane giełdowe dla wybranej korporacji z Alpha Vantage.

    :param company_name: Nazwa korporacji (np. 'Apple', 'Microsoft')
    :param api_key: Klucz API Alpha Vantage (domyślny: 'HRVCBXNVYPUS72OM')
    :param interval: Interwał czasowy (np. '5min', '15min', '1h')
    :return: DataFrame z danymi giełdowymi lub None w przypadku błędu
    """
    if company_name not in corp_symbol:
        print(f"Błąd: {company_name} nie znajduje się na liście obsługiwanych korporacji.")
        return None

    symbol = corp_symbol[company_name]
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={api_key}&datatype=csv'
    response = requests.get(url)

    if response.status_code == 200:
        # Konwersja danych na DataFrame
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        return df
    else:
        print(f"Nie udało się pobrać danych. Kod statusu: {response.status_code}")
        return None
