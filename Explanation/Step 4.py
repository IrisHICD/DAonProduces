# Averages of the three grain prices

from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter
import pandas as pd

data = pd.read_csv("32100077.csv")  

filtered_data = data[(data["GEO"] == "Alberta") &  
                     (data["Farm_products"].isin(["Oats [115113111]", "Barley [1151141]", "Rye [1151152]"]))]

filtered_data["REF_DATE"] = pd.to_datetime(filtered_data["REF_DATE"])

# Pivot the data so that each product has its own column
pivot_data = filtered_data.pivot_table(
    index="REF_DATE", 
    columns="Farm_products", 
    values="VALUE"
)

# Calculate the average price by date, considering missing values
pivot_data["Average_Price"] = pivot_data.mean(axis=1, skipna=True)

start_year = filtered_data["REF_DATE"].dt.year.min()
end_year = filtered_data["REF_DATE"].dt.year.max()

p = figure(
    title=f"Average Grain Prices in Alberta ({start_year} to {end_year})",
    x_axis_type="datetime",
    width=1000,
    height=500
)

p.line(pivot_data.index, pivot_data["Average_Price"], line_width=2, color="purple", legend_label="Average Price")

p.xaxis.axis_label = "Date"
p.yaxis.axis_label = "Price (Dollars per metric tonne)"

p.legend.location = "top_left"
p.legend.title = "Products"

# Format the x-axis to show readable dates
p.xaxis.formatter = DatetimeTickFormatter(months="%b %Y", years="%Y")
p.xaxis.major_label_orientation = 0.8

output_file("average_grain_prices_alberta.html")
show(p)
