import pandas as pd # type: ignore

data = pd.read_csv("32100077.csv")
# Quick look at the data and decided to drop a couple of useless columns
data.drop(columns=["DECIMALS", "TERMINATED", "DGUID"], inplace=True)
data.drop(columns=["STATUS", "SYMBOL", "VECTOR"], inplace=True)
data.info()

# Decided to focus on one grain at a time
barley_data = data[data["Farm products"].str.contains(r'\b\w*Barley\w*\b', regex=True)]
barley_data.info()
barley_counts = barley_data["Farm products"].value_counts()
print(barley_counts)
# At this point I noticed there are three kind of barley

barley_counts.head()



