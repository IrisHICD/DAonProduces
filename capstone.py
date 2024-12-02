import pandas as pd
# Step-by-Step Test Run
data = pd.read_csv("32100077.csv")
# Quick look at the data and decided to drop a couple of useless columns
data.drop(columns=["DECIMALS", "TERMINATED", "DGUID"], inplace=True)
data.drop(columns=["STATUS", "SYMBOL", "VECTOR"], inplace=True)

# Investigation steps
# Decided to focus on one grain at a time
barley_data = data[data["Farm products"].str.contains(r'\b\w*Barley\w*\b', regex=True)]
barley_data.info()
barley_counts = barley_data["Farm products"].value_counts()
print(barley_counts)
# At this point I noticed there are three kind of barley, wrote filtered code for only barley [1151141]
# I also want to selected out the only AB from GEO, need to make sure there are entries for AB
GEO_data = filtered_data["GEO"].value_counts()
print(GEO_data)
# it showed 630 entries for AB, great
# filtered code to focus on barley

filtered_data = data[data["Farm_products"].isin([
    "Barley [1151141]"
])]
# Barley only resulted in 4293 rows
filtered_data2 = filtered_data[(filtered_data["GEO"]== "Alberta")]
filtered_data2.info()
# filtering only AB resulted in 477 rows
filtered_data2.to_excel("filtered_data2.xlsx", index=False)
# Then I created the first graph for AB Barley



from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter
import pandas as pd

data = pd.read_excel("filtered_data2.xlsx") 
filtered_graph = data[["REF_DATE", "VALUE"]].copy()

# Convert REF_DATE to a datetime object for better handling
filtered_graph["REF_DATE"] = pd.to_datetime(filtered_graph["REF_DATE"])

# Create a Bokeh plot
start_year = filtered_graph["REF_DATE"].dt.year.min()
end_year = filtered_graph["REF_DATE"].dt.year.max()

p = figure(
    title=f"Barley price from year {start_year} to year {end_year}",
    x_axis_type="datetime",
    width=800,
    height=400
)

# Add line and circle markers
p.line(filtered_graph["REF_DATE"], filtered_graph["VALUE"], line_width=2, color="blue", legend_label="Barley Price")
p.circle(filtered_graph["REF_DATE"], filtered_graph["VALUE"], size=6, color="red", legend_label="Price Points")

# Add labels and legend
p.xaxis.axis_label = "Year"
p.yaxis.axis_label = "Price (Dollars per metric tonne)"
p.legend.location = "top_left"
p.legend.title = "Legend"

# Format the x-axis to show readable dates
p.xaxis.formatter = DatetimeTickFormatter(months="%b %Y", years="%Y")
p.xaxis.major_label_orientation = 0.8

# Save the graph to an HTML file and display it
output_file("barley_price_graph.html")
show(p)


# Final code
from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter
import pandas as pd

# Load the data
data = pd.read_csv("32100077.csv")  

# Filter data for Alberta and the selected products
filtered_data = data[(data["GEO"] == "Alberta") &  
                     (data["Farm_products"].isin(["Oats [115113111]", "Barley [1151141]", "Rye [1151152]"]))]

# Convert REF_DATE to a datetime object
filtered_data["REF_DATE"] = pd.to_datetime(filtered_data["REF_DATE"])

# Create a Bokeh plot
start_year = filtered_data["REF_DATE"].dt.year.min()
end_year = filtered_data["REF_DATE"].dt.year.max()

p = figure(
    title=f"Comparison of Oat, Barley, and Rye Prices in Alberta ({start_year} to {end_year})",
    x_axis_type="datetime",
    width=1000,
    height=500
)

# Plot each product 
colors = {"Oats [115113111]": "green", "Barley [1151141]": "blue", "Rye [1151152]": "red"}
for product, color in colors.items():
    product_data = filtered_data[filtered_data["Farm_products"] == product]
    p.line(product_data["REF_DATE"], product_data["VALUE"], line_width=2, color=color, legend_label=product.split(" [")[0])

# Add labels
p.xaxis.axis_label = "Date"
p.yaxis.axis_label = "Price (Dollars per metric tonne)"

# Move the legend to the top-left corner
p.legend.location = "top_left"
p.legend.title = "Products"

# Format the x-axis to show readable dates
p.xaxis.formatter = DatetimeTickFormatter(months="%b %Y", years="%Y")
p.xaxis.major_label_orientation = 0.8

# Save the graph to an HTML file and display it
output_file("alberta_product_comparison.html")
show(p)