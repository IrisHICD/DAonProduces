import pandas as pd
data = pd.read_csv("32100077.csv")

data.drop(columns=["DECIMALS", "TERMINATED", "DGUID"], inplace=True)
data.drop(columns=["STATUS", "SYMBOL", "VECTOR"], inplace=True)

data.info()

barley_data = data[data["Farm products"].str.contains(r'\b\w*Barley\w*\b', regex=True)]
barley_data.info()
barley_counts = barley_data["Farm products"].value_counts()