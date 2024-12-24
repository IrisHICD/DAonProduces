# Cattle 

from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter, CheckboxGroup, CustomJS
import pandas as pd
from bokeh.layouts import column

# Load the data
data = pd.read_csv("32100077.csv")  

# Filter data for Alberta and the selected products
filtered_data = data[(data["GEO"] == "Alberta") &  
                     (data["Farm_products"].isin([
                         "Cows for slaughter [111111111]", 
                         "Steers for slaughter [111111113]", 
                         "Heifers for slaughter [111111114]",
                         "Cattle for feeding [11111112]", 
                         "Calves for feeding [11111122]",
                         "Cattle for slaughter [11111111]", 
                         "Calves for slaughter [111111211]"
                     ]))]

# Convert REF_DATE to a datetime object
filtered_data["REF_DATE"] = pd.to_datetime(filtered_data["REF_DATE"])

# Create a Bokeh plot
start_year = filtered_data["REF_DATE"].dt.year.min()
end_year = filtered_data["REF_DATE"].dt.year.max()

p = figure(
    title=f"Comparison of Prices for Different Products in Alberta ({start_year} to {end_year})",
    x_axis_type="datetime",
    width=1500,
    height=800
)

# Plot each product 
products = {
    "Cows for slaughter [111111111]": "green",
    "Steers for slaughter [111111113]": "blue",
    "Heifers for slaughter [111111114]": "red",
    "Cattle for feeding [11111112]": "orange",
    "Calves for feeding [11111122]": "purple",
    "Cattle for slaughter [11111111]": "cyan",
    "Calves for slaughter [111111211]": "magenta"
}

lines = {}
for product, color in products.items():
    product_data = filtered_data[filtered_data["Farm_products"] == product]
    line = p.line(product_data["REF_DATE"], product_data["VALUE"], line_width=2, color=color, legend_label=product.split(" [")[0])
    lines[product] = line

# Add labels
p.xaxis.axis_label = "Date"
p.yaxis.axis_label = "Price (Dollars per metric tonne)"

# Move the legend to the top-left corner
p.legend.location = "top_left"
p.legend.title = "Products"

# Format the x-axis to show readable dates
p.xaxis.formatter = DatetimeTickFormatter(months="%b %Y", years="%Y")
p.xaxis.major_label_orientation = 0.8

# Create a checkbox group for each product
checkbox = CheckboxGroup(
    labels=list(products.keys()),
    active=[0, 1, 2, 3, 4, 5, 6]  # Initially, all are selected
)

# Create a JavaScript callback to show/hide lines based on checkbox selection
callback = CustomJS(args=dict(lines=lines), code="""
    var active = cb_obj.active;
    for (var product in lines) {
        lines[product].visible = false;
    }
    for (var i = 0; i < active.length; i++) {
        var product = cb_obj.labels[active[i]];
        lines[product].visible = true;
    }
""")

checkbox.js_on_change('active', callback)

# Layout the checkbox and the plot together
layout = column(checkbox, p)

# Save the graph to an HTML file and display it
output_file("alberta_cattle_interactive_comparison.html")
show(layout)
