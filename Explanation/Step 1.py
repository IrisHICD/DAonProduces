import pandas as pd
# STEP 1 investigation
data = pd.read_csv("32100077.csv")
print(data.head())

# Quick look at the data and decided to drop a couple of useless columns
data.drop(columns=["DECIMALS", "TERMINATED", "DGUID"], inplace=True)
data.drop(columns=["STATUS", "SYMBOL", "VECTOR"], inplace=True)

# How much different products are there? 
data2 = data["Farm_products"].value_counts()
data2.info()
print(data2)

# Decided to focus on one grain at a time
barley_data = data[data["Farm_products"].str.contains(r'\b\w*Barley\w*\b', regex=True)]
barley_data.info()
barley_counts = barley_data["Farm_products"].value_counts()
print(barley_counts)
# At this point I noticed there are three kind of barley, need to write filtered code for only barley [1151141]
# I also want to selected out the only AB from GEO, need to make sure there are entries for AB
GEO_data = barley_data["GEO"].value_counts()
print(GEO_data)
# GEO had all the provinces, only want to focus on AB

filtered_data = data[data["Farm_products"].isin([
    "Barley [1151141]"
])]
# Barley only resulted in 4293 rows
filtered_data2 = filtered_data[(filtered_data["GEO"]== "Alberta")]
filtered_data2.info()
# filtering only AB resulted in 477 rows
filtered_data2.to_excel("filtered_data2.xlsx", index=False)
# Then I created the first graph for AB Barley in STEP 2
