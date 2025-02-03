## The following application is in no way a financial advice, was created solely for educational purposes and should be used only for such cases.

# Trade Advisor
A simple trade advisor.

## Description

A simple trade advisor using a LSTM model, capable of:

 - downloading up-to-date stock data and calculating various technical indicators,
 - plotting historic data,
 - calculating potential profit or loss for a given company and timespan,
 - plotting predictions.

Currently supported companies:
  - Apple
  - Amazon
  - Meta
  - Microsoft
  - Alphabet (Google)

Currently supported stock indexes:
  - S&P500
## Setup

Firstly, download and install requirements for TA-Lib, following the guide on this repository: [TA-Lib/ta-lib-python: Python wrapper for TA-Lib).](https://github.com/TA-Lib/ta-lib-python)

Clone the repository (the application won't work if it's not inside a git repository):
```bash
	git clone https://github.com/aszym68/bot_projekt/
```

Afterwards, install the requirements using:
```bash
	pip install -r requirements.txt
 ```
 To re-train the model, run the following from the root directory of the project:
 ``` bash
	 python -m models.model
 ```
To launch the main GUI (from the root directory) use:
```bash
	python main.py
```
# Screenshots
![Prediction plotting](https://i.imgur.com/JgkC4wp.png)

![technical indicators plotting](https://i.imgur.com/plJMu6F.png)
