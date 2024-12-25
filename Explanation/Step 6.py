# Testing side widget with annual average

from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter, CheckboxGroup, CustomJS, Slider, Select, Div, ColumnDataSource
from bokeh.layouts import column, row
import pandas as pd

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

# Slider to select the year
slider = Slider(start=start_year, end=end_year, value=start_year, step=1, title="Select Year")

# Dropdown (Select) to choose the cattle type
cattle_select = Select(title="Select Cattle Type", value="Cows for slaughter [111111111]", options=list(products.keys()))

# Div widget to display the average price
average_price_display = Div(text=f"<b>Average Price for {cattle_select.value} in {slider.value}:</b> $0.00", width=300, height=30)

# Create a ColumnDataSource to pass the data to JS
source = ColumnDataSource(filtered_data)

# JavaScript callback to update the average price
average_price_callback = CustomJS(args=dict(source=source, slider=slider, cattle_select=cattle_select, average_price_display=average_price_display), code="""
    var selected_year = slider.value;
    var selected_cattle_type = cattle_select.value;
    var data = source.data;
    
    var total = 0;
    var count = 0;
    
    // Loop through the data and calculate the average for the selected cattle type and year
    for (var i = 0; i < data['REF_DATE'].length; i++) {
        var year = new Date(data['REF_DATE'][i]).getFullYear();
        if (year === selected_year && data['Farm_products'][i] === selected_cattle_type) {
            total += data['VALUE'][i];
            count++;
        }
    }
    
    // Calculate the average
    var average_price = (count > 0) ? total / count : 0;
    average_price_display.text = "<b>Average Price for " + selected_cattle_type + " in " + selected_year + ":</b> $" + average_price.toFixed(2);
""")

# Attach the callback to the slider and the select dropdown
slider.js_on_change('value', average_price_callback)
cattle_select.js_on_change('value', average_price_callback)

# Arrange everything (checkbox, plot, and widgets) in a layout
layout = row(
    column(checkbox, p),  # Plot and checkbox on the left
    column(slider, cattle_select, average_price_display)  # Widgets on the right
)

# Save the graph to an HTML file and display it
output_file("alberta_cattle_interactive_comparison.html")
show(layout)
