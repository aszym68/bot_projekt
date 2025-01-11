import requests
from symbols import corp_symbol

def fetch_fundamental_data(company_name, api_key='HRVCBXNVYPUS72OM'):
    """
    Pobiera wskaźniki fundamentalne z Alpha Vantage (OVERVIEW endpoint).

    :param company_name: Nazwa korporacji (np. 'Apple', 'Microsoft')
    :param api_key: Klucz API Alpha Vantage.
    :return: Słownik z danymi fundamentalnymi lub None w przypadku błędu.

    """

    if company_name not in corp_symbol:
        print(f"Błąd: {company_name} nie znajduje się na liście obsługiwanych korporacji.")
        return None

    symbol = corp_symbol[company_name]
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "Symbol" in data:
            return {
                # Podstawowe wskaźniki fundamentalne
                "MarketCap": data.get("MarketCapitalization"),  # Kapitalizacja rynkowa
                "PERatio": data.get("PERatio"),  # Stosunek ceny do zysku
                "PEGRatio": data.get("PEGRatio"),  # Stosunek ceny do zysku z uwzględnieniem wzrostu
                "EPS": data.get("EPS"),  # Zysk na akcję
                "DividendYield": data.get("DividendYield"),  # Stopa dywidendy
                "DividendPerShare": data.get("DividendPerShare"),  # Dywidenda na akcję
                "RevenueTTM": data.get("RevenueTTM"),  # Przychody za ostatnie 12 miesięcy
                "ProfitMargin": data.get("ProfitMargin"),  # Marża zysku netto
                "OperatingMarginTTM": data.get("OperatingMarginTTM"),  # Marża operacyjna za ostatnie 12 miesięcy

                # Wskaźniki finansowe
                "EBITDA": data.get("EBITDA"),  # Zysk operacyjny przed odsetkami, podatkami, deprecjacją i amortyzacją
                "GrossProfitTTM": data.get("GrossProfitTTM"),  # Zysk brutto za ostatnie 12 miesięcy
                "OperatingIncomeTTM": data.get("OperatingIncomeTTM"),  # Dochód operacyjny za ostatnie 12 miesięcy
                "ReturnOnAssetsTTM": data.get("ReturnOnAssetsTTM"),  # Zwrot z aktywów
                "ReturnOnEquityTTM": data.get("ReturnOnEquityTTM"),  # Zwrot z kapitału własnego
                "BookValue": data.get("BookValue"),  # Wartość księgowa na akcję
                "EnterpriseValue": data.get("EnterpriseValue"),  # Wartość przedsiębiorstwa
                "EVToRevenue": data.get("EVToRevenue"),  # EV/Revenue
                "EVToEBITDA": data.get("EVToEBITDA"),  # EV/EBITDA

                # Dane bilansowe
                "TotalDebt": data.get("TotalDebt"),  # Całkowite zadłużenie
                "TotalCash": data.get("TotalCash"),  # Całkowita gotówka
                "TotalRevenue": data.get("TotalRevenue"),  # Całkowite przychody
                "SharesOutstanding": data.get("SharesOutstanding"),  # Liczba akcji w obiegu

                # Wskaźniki dodatkowe
                "TrailingPE": data.get("TrailingPE"),  # Stosunek ceny do zysku za ostatnie 12 miesięcy
                "ForwardPE": data.get("ForwardPE"),  # Prognozowany stosunek ceny do zysku
                "PriceToBookRatio": data.get("PriceToBookRatio"),  # Cena do wartości księgowej
                "PriceToSalesRatioTTM": data.get("PriceToSalesRatioTTM"),  # Cena do przychodów za ostatnie 12 miesięcy
                "QuarterlyEarningsGrowthYOY": data.get("QuarterlyEarningsGrowthYOY"),  # Wzrost zysku kwartalnego r/r
                "QuarterlyRevenueGrowthYOY": data.get("QuarterlyRevenueGrowthYOY"),  # Wzrost przychodów kwartalnych r/r
                "PayoutRatio": data.get("PayoutRatio")  # Wskaźnik wypłaty dywidendy
            }

        else:
            print("Brak danych dla podanego symbolu.")
            return None
    else:
        print(f"Nie udało się pobrać danych. Kod statusu: {response.status_code}")
        return None
