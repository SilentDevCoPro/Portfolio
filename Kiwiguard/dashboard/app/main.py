import os
import requests
import pandas as pd
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import logging
import json

# Initialize the Dash app
app = Dash(__name__)

# Initialize an empty DataFrame
df = pd.DataFrame()

# Layout of the Dash app
app.layout = html.Div([
    html.H1("System Metrics Dashboard"),
    dcc.Dropdown(
        id='metric-dropdown',
        options=[
            {'label': 'CPU Percent', 'value': 'cpu_percent'},
            {'label': 'Memory Percent', 'value': 'memory_percent'},
            {'label': 'Disk Percent', 'value': 'disk_percent'},
            # Add other metrics as needed
        ],
        value='cpu_percent'  # default value
    ),
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # Update every 5 seconds
        n_intervals=0  # start at zero
    )
])

# Global DataFrame to store data
global_df = pd.DataFrame()

# Callback to update data and graph
@app.callback(
    Output('live-graph', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('metric-dropdown', 'value')]
)
def update_graph_live(n, selected_metric):
    global global_df

    # Fetch data from the Collector
    collector_host = os.getenv('COLLECTOR_HOST', 'localhost')
    collector_port = os.getenv('COLLECTOR_PORT', '5000')
    collector_url = f'http://{collector_host}:{collector_port}/metrics'

    try:
        response = requests.get(collector_url)
        data = response.json()

        # Convert timestamp to datetime for better plotting
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')

        # Append new data to the global DataFrame
        global_df = global_df.append(data, ignore_index=True)
    except Exception as e:
        print(f"Error fetching data: {e}")

    # Create the figure
    fig = px.line(global_df, x='timestamp', y=selected_metric)
    fig.update_layout(title=f"{selected_metric} Over Time")

    return fig

def load_config():
    """
    Loads the application configuration from a 'config.json' file.
    If the file cannot be found or parsed, the process is terminated with an error log.

    Returns:
        dict: The loaded configuration from the JSON file.

    Logs:
        - Error details if the configuration file fails to load.
    """
    try:
        with open('config.json') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f'Error loading config file: {e}')
        exit(1)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    config = load_config()
    interval = config.get('interval', 60)
    collector_url = config.get('collector_url')

    if not collector_url:
        logging.error("Collector URL not specified in agent/app/config.json")
        exit(1)

    app.run_server(debug=True, host='dashboard', port=8050)

if __name__ == '__main__':
    main()
