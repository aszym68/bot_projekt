import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from fetch_data import symbols as sym
from fetch_data import config as cfg
from fetch_data import utils


results_path = utils.get_repo_path() / cfg.MODELS_PATH /  'results_lstm.csv'
results_df = pd.read_csv(results_path)


best_per_symbol = results_df.loc[results_df.groupby("Symbol")["MSE"].idxmin()]
print("\nNajlepszy model dla każdego symbolu:")
print(best_per_symbol)

