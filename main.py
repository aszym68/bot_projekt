# TO DO:
# technical indicators layout


import json
import sys
from tkinter import messagebox as mb
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QTabWidget,
    QComboBox,
    QSpinBox,
    QMessageBox,
)
from PyQt5.QtGui import QPixmap, QIcon
from fetch_data import fetch_stock_data as download
from fetch_data import symbols as sym
from fetch_data import config as cfg
from fetch_data import utils
from plots import plots
from models.model import StockModel


class Advisor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.already_calculated = {}
        self.predicted_prices = {}
        for symbol in self.get_companies():
            self.already_calculated[symbol] = (
                False  # this will help us keep track of what has been already calculated so then we can block the user from potentially trying to plot uncalculated data
            )
            self.predicted_prices[symbol] = None  # for storing the predictions
        self.setWindowTitle("Trade Advisor")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(
            QIcon(str(utils.get_repo_path() / cfg.ICON_PATH / cfg.ICON_FILE))
        )
        # Main Layout
        main_layout = QVBoxLayout()

        # Input Fields Layout
        input_layout = QHBoxLayout()

        self.capital_input = QLineEdit(self)
        self.capital_input.setPlaceholderText("Enter your capital...")

        self.index_selector = QComboBox(self)
        self.index_selector.addItems(self.get_companies())
        self.index_selector.currentIndexChanged.connect(self.update_button_state)

        self.days_input = QSpinBox(self)
        self.days_input.setRange(20, 365)
        self.days_input.setPrefix("Days: ")

        input_layout.addWidget(self.capital_input)
        input_layout.addWidget(self.index_selector)
        input_layout.addWidget(self.days_input)

        buttons_layout = QHBoxLayout()

        self.calculate_button = QPushButton("Calculate")

        self.calculate_button.clicked.connect(self.calculate_advice)

        buttons_layout.addWidget(self.calculate_button)

        # Tabs
        self.tabs = QTabWidget()
        self.tab_a = QWidget()
        self.tab_b = QWidget()
        self.tab_c = QWidget()

        self.tabs.addTab(self.tab_a, "Historic prices")
        self.tabs.addTab(self.tab_b, "Technical indicators")
        self.tabs.addTab(self.tab_c, "Predictions")
        # TAB A
        tab_a_layout = QVBoxLayout()
        self.plot_days_a = QSpinBox(self)
        self.plot_days_a.setRange(30, 1825)
        self.plot_days_a.setPrefix("Days: ")

        self.plot_button_a = QPushButton("Show")
        self.plot_button_a.clicked.connect(self.graph_stocks)
        self.graph_label_a = QLabel(self)
        self.graph_label_a.setAlignment(Qt.AlignCenter)

        tab_a_layout.addWidget(self.graph_label_a)
        tab_a_layout.addWidget(self.plot_days_a)
        tab_a_layout.addWidget(self.plot_button_a)

        self.tab_a.setLayout(tab_a_layout)

        # TAB B
        tab_b_layout = QVBoxLayout()
        self.indicator_selector = QComboBox(self)
        self.indicator_selector.addItems(self.get_tech_indicators())
        self.plot_days_b = QSpinBox(self)
        self.plot_days_b.setRange(30, 1810)
        self.plot_days_b.setPrefix("Days: ")
        self.plot_button_b = QPushButton("Show")
        self.plot_button_b.clicked.connect(self.graph_technical)
        self.graph_label_b = QLabel(self)
        self.graph_label_b.setAlignment(Qt.AlignCenter)

        tab_b_layout.addWidget(self.graph_label_b)
        tab_b_layout.addWidget(self.indicator_selector)
        tab_b_layout.addWidget(self.plot_days_b)
        tab_b_layout.addWidget(self.plot_button_b)

        self.tab_b.setLayout(tab_b_layout)

        # TAB C
        tab_c_layout = QVBoxLayout()
        self.plot_days_c = QSpinBox(self)
        self.plot_days_c.setRange(30, 1810)
        self.plot_days_c.setPrefix("Previous days: ")
        self.plot_button_c = QPushButton("Show")
        self.update_button_state()
        self.plot_button_c.clicked.connect(self.graph_predictions)
        self.graph_label_c = QLabel(self)
        self.graph_label_c.setAlignment(Qt.AlignCenter)

        tab_c_layout.addWidget(self.graph_label_c)
        tab_c_layout.addWidget(self.plot_days_c)
        tab_c_layout.addWidget(self.plot_button_c)

        self.tab_c.setLayout(tab_c_layout)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def graph_stocks(self):
        symbol = self.index_selector.currentText()
        days = self.plot_days_a.value()
        buf = plots.plot_stock_prices(symbol, days)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.read())
        self.graph_label_a.setPixmap(pixmap)

    def graph_technical(self):
        symbol = self.index_selector.currentText()
        days = self.plot_days_b.value()
        buf = plots.plot_technical(symbol, days, self.indicator_selector.currentText())
        pixmap = QPixmap()
        pixmap.loadFromData(buf.read())
        self.graph_label_b.setPixmap(pixmap)

    def graph_predictions(self):
        symbol = self.index_selector.currentText()
        days = self.days_input.value()
        predictions = self.predicted_prices[symbol]
        buf = plots.plot_predicted(
            symbol, predictions, days, prev_days=self.plot_days_c.value()
        )
        pixmap = QPixmap()
        pixmap.loadFromData(buf.read())
        self.graph_label_c.setPixmap(pixmap)

    def get_companies(self):
        return list(sym.corp_symbol.values())

    def get_tech_indicators(self):
        return list(sym.technical_indicators.keys())

    def calculate_advice(self):
        capital = self.capital_input.text()
        if not capital.isdigit():
            mb.showwarning("Invalid Input", "Please enter a valid number for capital.")
            return

        capital = float(capital)
        symbol = self.index_selector.currentText()

        model = StockModel(symbol)
        try:
            model.load_data()
            model.prepare_data()
            model.load_trained_model()

            predicted_prices, advice = model.recommend_action()
            predictions = [
                predicted_prices[i][0] for i in range(len(predicted_prices) - 1)
            ]
            print(predictions)
            last_price = model.data["Close"].iloc[-1]
            potential_profit = capital * (predictions[-1] / last_price - 1)

            msg = QMessageBox(self)
            msg.setWindowTitle("Investment Advice")
            msg.setText(
                f"Recommendation for {symbol}: {advice}\nPotential profit: {potential_profit:.2f} USD"
            )
            self.already_calculated[symbol] = True
            self.update_button_state()
            self.predicted_prices[symbol] = predictions
            msg.setIcon(QMessageBox.Information)
            msg.show()  # Nie blokuje GUI!
        except Exception as e:
            mb.showwarning("Error", f"Could not calculate advice: {e}")

    def update_button_state(self):
        current_item = self.index_selector.currentText()
        self.plot_button_c.setEnabled(self.already_calculated[current_item])
        if not self.already_calculated[current_item]:
            self.plot_button_c.setToolTip(
                "First use the calculate button to calculate the predictions."
            )
        else:
            self.plot_button_c.setToolTip(None)


def main():
    with open(
        utils.get_repo_path() / cfg.CFG_FOLDER / cfg.CFG_JSON, "r"
    ) as config_file:
        try:
            config = json.load(config_file)
            update_date = config.get("last_download")
        except json.JSONDecodeError:
            print("Error reading config.json, cannot read last update date.")
            update_date = "unknown"
    res = mb.askquestion(
        "Redownload data",
        f"Do you want to update the index with current data? Last update date: {update_date}",
    )
    if res == "yes":
        download.main()
        gui()
    else:
        gui()


def gui():
    app = QApplication(sys.argv)
    window = Advisor()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
