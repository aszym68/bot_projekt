import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

from fetch_data import fetch_stock_data as download
from fetch_data import symbols as sym
from fetch_data import config as cfg
from fetch_data import utils


class StockModel:
    def __init__(self, symbol):

        self.symbol = symbol
        self.output_path = utils.get_repo_path() / cfg.OUTPUT_PATH
        self.repo_path = utils.get_repo_path()
        self.data = None
        self.model = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    def load_data(self):

        stock_file = self.repo_path / self.output_path / f"{self.symbol}.csv"
        tech_file = self.repo_path / self.output_path / f"{self.symbol}_tech.csv"

        data_stock = pd.read_csv(stock_file)
        data_tech = pd.read_csv(tech_file)

        self.data = pd.concat([data_stock, data_tech], axis=1)
        self.data = self.data.iloc[::-1]
        self.data['Change'] = (self.data['Close'] - self.data['Open']) / self.data['Open']

    def prepare_data(self):

        X = self.data[['SMA_20', 'EMA_20', 'BB_Upper', 'BB_Middle',
                       'BB_Lower', 'ADX_14', 'CCI_14', 'STOCH_K',
                       'STOCH_D', 'OBV', 'Change']].values
        y = self.data['Close'].values

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )

    def train(self):

        if self.X_train is None or self.y_train is None:
            raise ValueError("The training data has not been prepared. Run `prepare_data()`.")

        self.model = XGBRegressor()
        self.model.fit(self.X_train, self.y_train)

    def evaluate(self):

        if self.model is None:
            raise ValueError("The model has not been trained. Run `train()`.")

        y_pred = self.model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, y_pred)
        return mse

    def save_model(self, output_path):

        import joblib
        model_path = self.repo_path / output_path / f"{self.symbol}_model.pkl"
        joblib.dump(self.model, model_path)
        print(f"Model saved in {model_path}")

def main():
    results = []

    for index, symbol in enumerate(sym.corp_symbol.values()):
        print(f"Processing {symbol} ({index+1}/{len(sym.corp_symbol)})...")

        model = StockModel(symbol)

        try:
            model.load_data()
            model.prepare_data()
            model.train()
            mse = model.evaluate()
            print(f"{symbol}: MSE = {mse:.4f}")

            results.append({"Symbol": symbol, "MSE": mse})

            model.save_model(cfg.MODELS_PATH)

        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            results.append({"Symbol": symbol, "MSE": None})

    results_df = pd.DataFrame(results)
    results_path = model.repo_path / cfg.OUTPUT_PATH / "results.csv"
    results_df.to_csv(results_path, index=False)
    print(f"Results saved to {results_path}")


if __name__ == "__main__":
    main()
