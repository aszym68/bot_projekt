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
)
from PyQt5.QtGui import QPixmap
from fetch_data import fetch_stock_data as download
from fetch_data import symbols as sym
from fetch_data import config as cfg
from fetch_data import utils
from plots import plots


class Advisor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Trade Advisor")
        self.setGeometry(100, 100, 600, 400)

        # Main Layout
        main_layout = QVBoxLayout()

        # Input Fields Layout
        input_layout = QHBoxLayout()

        self.capital_input = QLineEdit(self)
        self.capital_input.setPlaceholderText("Enter your capital...")

        self.index_selector = QComboBox(self)
        self.index_selector.addItems(self.get_companies())

        self.days_input = QSpinBox(self)
        self.days_input.setRange(20, 365)
        self.days_input.setPrefix("Days: ")

        input_layout.addWidget(self.capital_input)
        input_layout.addWidget(self.index_selector)
        input_layout.addWidget(self.days_input)

        # Buttons Layout
        buttons_layout = QHBoxLayout()

        self.calculate_button = QPushButton("Calculate")
        self.add_button = QPushButton("Add another!")

        self.calculate_button.clicked.connect(self.show_graph)

        buttons_layout.addWidget(self.calculate_button)
        buttons_layout.addWidget(self.add_button)

        # Tabs
        self.tabs = QTabWidget()
        self.tab_a = QWidget()
        self.tab_b = QWidget()
        self.tab_c = QWidget()

        # Set up individual tabs
        self.tabs.addTab(self.tab_a, "Show historic prices")
        self.tabs.addTab(self.tab_b, "Technical indicators")
        self.tabs.addTab(self.tab_c, "Tab C")

        # Tab content example
        tab_a_layout = QVBoxLayout()

        self.graph_label = QLabel(self)
        self.graph_label.setAlignment(Qt.AlignCenter)

        tab_a_layout.addWidget(self.graph_label)

        self.tab_a.setLayout(tab_a_layout)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    def show_graph(self):
        symbol = self.index_selector.currentText()
        days = self.days_input.value()
        buf = plots.plot_stock_prices(symbol, days)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.read())
        self.graph_label.setPixmap(pixmap)

    def get_companies(self):
        return list(sym.corp_symbol.values())


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
