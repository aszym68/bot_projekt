import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

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
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    def load_data(self):
        stock_file = self.repo_path / self.output_path / f"{self.symbol}.csv"
        tech_file = self.repo_path / self.output_path / f"{self.symbol}_tech.csv"

        data_stock = pd.read_csv(stock_file)
        data_tech = pd.read_csv(tech_file)

        self.data = pd.concat([data_stock, data_tech], axis=1)
        self.data = self.data.iloc[::-1]
        self.data['Change'] = (self.data['Close'] - self.data['Open']) / self.data['Open']

        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        numeric_cols = [col for col in numeric_cols if not col.startswith("Unnamed")]
        non_numeric_cols = self.data.select_dtypes(exclude=[np.number]).columns

        self.data = self.data[numeric_cols]

    def prepare_data(self, sequence_length=30):
        scaled_data = self.scaler.fit_transform(self.data[['Close']].values)

        X, y = [], []
        for i in range(sequence_length, len(scaled_data)):
            X.append(scaled_data[i-sequence_length:i, 0])
            y.append(scaled_data[i, 0])

        X, y = np.array(X), np.array(y)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )

        self.X_train = np.reshape(self.X_train, (self.X_train.shape[0], self.X_train.shape[1], 1))
        self.X_test = np.reshape(self.X_test, (self.X_test.shape[0], self.X_test.shape[1], 1))

    def build_model(self):

        optimizer = Adam(learning_rate=0.001)

        self.model = Sequential([
            LSTM(units=128, return_sequences=True, input_shape=(self.X_train.shape[1], 1)),
            Dropout(0.2),
            LSTM(units=128, return_sequences=False),
            Dropout(0.2),
            Dense(units=25),
            Dense(units=1)
        ])
        self.model.compile(optimizer=optimizer, loss='mean_squared_error')

    def train(self, epochs=20, batch_size=16):
        if self.X_train is None or self.y_train is None:
            raise ValueError("The training data has not been prepared. Run `prepare_data()`.")

        if self.model is None:
            raise ValueError("The model has not been built. Run `build_model()`.")

        self.model.fit(self.X_train, self.y_train, epochs=epochs, batch_size=batch_size)

    def evaluate(self):
        if self.model is None:
            raise ValueError("No model has been trained. Run `train()`.")

        predictions = self.model.predict(self.X_test)
        predictions = self.scaler.inverse_transform(predictions)
        y_test_rescaled = self.scaler.inverse_transform(self.y_test.reshape(-1, 1))

        mse = mean_squared_error(y_test_rescaled, predictions)
        mae = mean_absolute_error(y_test_rescaled, predictions)
        r2 = r2_score(y_test_rescaled, predictions)

        return {"MSE": mse, "MAE": mae, "R2": r2}

    def save_model(self, output_path):
        model_path = self.repo_path / output_path / f"{self.symbol}_LSTM_model.h5"
        self.model.save(model_path)
        print(f"LSTM model saved in {model_path}")


    def recommend_action(self, lookback=5):
        if self.model is None:
            raise ValueError("The model is not loaded")

        predictions = self.model.predict(self.X_test)
        predictions = self.scaler.inverse_transform(predictions)
        y_test_rescaled = self.scaler.inverse_transform(self.y_test.reshape(-1, 1))

        last_prices = y_test_rescaled[-lookback:].flatten()
        predicted_prices = predictions[-lookback:].flatten()

        avg_actual = np.mean(last_prices)
        avg_predicted = np.mean(predicted_prices)
        change_percentage = (avg_predicted - avg_actual) / avg_actual * 100

        if change_percentage > 2:
            return "Buy"
        elif change_percentage < -2:
            return "Sell"
        else:
            return "Hold"

    def load_trained_model(self):
        model_path = self.repo_path / cfg.MODELS_PATH / f"{self.symbol}_LSTM_model.h5"
        if not model_path.exists():
            raise FileNotFoundError(f"Model {self.symbol} not found.")
        self.model = load_model(model_path)


def main():
    all_results = []

    for index, symbol in enumerate(sym.corp_symbol.values()):
        print(f"Processing {symbol} ({index + 1}/{len(sym.corp_symbol)})...")

        model = StockModel(symbol)

        try:
            model.load_data()
            model.prepare_data()
            model.build_model()
            model.train(epochs=20, batch_size=32)
            results = model.evaluate()

            print(
                f"{symbol} (LSTM): MSE = {results['MSE']:.4f}, MAE = {results['MAE']:.4f}, R2 = {results['R2']:.4f}")

            all_results.append({"Symbol": symbol, "Model": "LSTM", **results})

            model.save_model(cfg.MODELS_PATH)

        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            all_results.append({"Symbol": symbol, "Model": None, "MSE": None, "MAE": None, "R2": None})

    results_df = pd.DataFrame(all_results)
    results_path = model.repo_path / cfg.MODELS_PATH / "results_lstm.csv"
    results_df.to_csv(results_path, index=False)
    print(f"Results saved to {results_path}")


if __name__ == "__main__":
    main()

