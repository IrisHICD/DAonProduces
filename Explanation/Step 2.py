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
p.legend.title = "Legend"

# Format the x-axis to show readable dates
p.xaxis.formatter = DatetimeTickFormatter(months="%b %Y", years="%Y")
p.xaxis.major_label_orientation = 0.8

# Save the graph to an HTML file and display it
output_file("barley_price_graph.html")
show(p)
