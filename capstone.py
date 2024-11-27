import pandas as pd
# from bokeh.plotting import figure, show, output_notebook
# from bokeh.models import ColumnDataSource
# output_notebook()

data = pd.read_csv("32100077.csv")
# Quick look at the data and decided to drop a couple of useless columns
data.drop(columns=["DECIMALS", "TERMINATED", "DGUID"], inplace=True)
data.drop(columns=["STATUS", "SYMBOL", "VECTOR"], inplace=True)

# filtered code
filtered_data = data[data["Farm_products"].isin([
    "Barley [1151141]",
    "Barley for animal feed [115114111]"
])]
filtered_data.info()

# Investigation steps
# Decided to focus on one grain at a time
barley_data = data[data["Farm products"].str.contains(r'\b\w*Barley\w*\b', regex=True)]
barley_data.info()
barley_counts = barley_data["Farm products"].value_counts()
print(barley_counts)
# At this point I noticed there are three kind of barley, wrote filtered code
# I also want to selected out the only AB from GEO, need to make sure there are entries for AB
GEO_data = filtered_data["GEO"].value_counts()
print(GEO_data)
# it showed 630 entries for AB, great

