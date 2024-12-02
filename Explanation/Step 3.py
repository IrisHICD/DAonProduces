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