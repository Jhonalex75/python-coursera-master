import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Sample data
data = {
    "Product": ["A", "B", "C", "D"],
    "Sales": [100, 200, 300, 400]
}
df = pd.DataFrame(data)

# Create a bar chart with Plotly Express
fig = px.bar(df, x="Product", y="Sales", title="Sales by Product")

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Simple Dash Example"),
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)