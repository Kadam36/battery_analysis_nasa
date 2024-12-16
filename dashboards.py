# from ast import arg
# import os
# import pandas as pd
# import plotly.graph_objects as go
# from dash import Dash, html, dcc

# # Paths
# data_directory = r"/home/kadam36/battery_analysis_nasa/battery_dataset/data"

# # Dash app
# app = Dash(__name__)
# app.title = "Battery Dataset Dashboard"

# # Global data storage for the dashboard
# plots = []

# def load_csv(file_name):
#     """Load a specific CSV file."""
#     file_path = os.path.join(data_directory, file_name)
#     data = pd.read_csv(file_path)
#     print(f"Loaded file: {file_name}")
#     print(data.head())
#     return data

# def create_plot(data, x_column, y_column, title):
#     """Create a customized plot for the dashboard."""
#     if x_column in data.columns and y_column in data.columns:
#         fig = go.Figure()

#         # Add trace
#         fig.add_trace(go.Scatter(
#             x=data[x_column],
#             y=data[y_column],
#             mode='lines+markers',  
#             name=f'{y_column} vs {x_column}',  
#             line=dict(width=2, dash='solid', color='royalblue'), 
#             marker=dict(size=6, color='red', symbol='circle', opacity=0.7), 
#             hoverinfo='text',  
#             hovertext=data.apply(lambda row: f"{x_column}: {row[x_column]}<br>{y_column}: {row[y_column]}", axis=1)
#         ))

#         # Update layout
#         fig.update_layout(
#             title=title,
#             xaxis_title=x_column,
#             yaxis_title=y_column,
#             template='plotly_dark',
#             hovermode='closest',
#             showlegend=True,
#             legend=dict(
#                 title="Legend",
#                 x=0.85,
#                 y=0.95,
#                 bgcolor='rgba(255, 255, 255, 0.5)',
#                 bordercolor='black',
#                 borderwidth=1
#             )
#         )
#         return fig
#     else:
#         print(f"Skipping plot: Required columns {x_column}, {y_column} not found.")
#         return None

# def process_all_files(limit=None):
#     """Process all files in the dataset with an optional limit."""
#     csv_files = [f for f in os.listdir(data_directory) if f.endswith('.csv')]
    
#     if limit:
#         csv_files = csv_files[:limit]
    
#     for file_name in csv_files:
#         data = load_csv(file_name)

#         # Add plots for the dashboard
#         plots.append({
#             "file_name": file_name,
#             "figures": [
#                 create_plot(data, x_column='Time', y_column='Voltage_measured', title=f"Voltage vs Time ({file_name})"),
#                 create_plot(data, x_column='Time', y_column='Current_measured', title=f"Current vs Time ({file_name})"),
#                 create_plot(data, x_column='Time', y_column='Battery_impedance', title=f"Impedance vs Time ({file_name})"),
#                 create_plot(data, x_column='Time', y_column='Temperature_measured', title=f"Temperature vs Time ({file_name})")
#             ]
#         })

# # Load and process data
# process_all_files(limit=3)  # Limit to 3 files for the dashboard

# # Define the layout for the Dash app
# app.layout = html.Div([
#     html.H1("Battery Dataset Dashboard", style={'textAlign': 'center', 'color': 'white'}),
#     html.Div(style={'margin': '20px'}),  # Add some spacing

#     # Add each file's plots to the dashboard
#     *[
#         html.Div([
#             html.H2(f"File: {plot['file_name']}", style={'color': 'cyan'}),
#             *[
#                 dcc.Graph(figure=fig) for fig in plot['figures'] if fig is not None
#             ]
#         ], style={'marginBottom': '50px', 'border': '1px solid white', 'padding': '10px'})
#         for plot in plots
#     ]
# ], style={'backgroundColor': '#111111', 'color': 'white', 'padding': '20px'})

# # Run the Dash app
# if __name__ == "__main__":
#     app.run_server(debug=True)




import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
app.title = "CSV Data Dashboard"

data_directory = r"C:\Users\user\.cache\kagglehub\datasets\patrickfleith\nasa-battery-dataset\versions\2\cleaned_dataset\data"

data_store = {}
available_columns = set()

def load_csv(file_name):
    """Load a CSV file and log its columns."""
    file_path = os.path.join(data_directory, file_name)
    try:
        data = pd.read_csv(file_path)
        print(f"Loaded file: {file_name}")
        print(f"Columns: {data.columns.tolist()}")
        print(data.head())
        return data
    except Exception as e:
        print(f"Error loading {file_name}: {e}")
        return None

def load_all_csv_files():
    """Load all CSV files from the directory."""
    csv_files = [f for f in os.listdir(data_directory) if f.endswith('.csv')]
    for file_name in csv_files[:10]:  # Limit to 10 files
        data = load_csv(file_name)
        if data is not None:
            data_store[file_name] = data
            available_columns.update(data.columns.tolist())

load_all_csv_files()

# Dash layout
app.layout = html.Div([
    html.H1("CSV Data Dashboard", style={"textAlign": "center"}),
    
    html.Div([
        html.Label("Select File:"),
        dcc.Dropdown(
            id="file-dropdown",
            options=[{"label": file, "value": file} for file in data_store.keys()],
            value=list(data_store.keys())[0] if data_store else None,
        ),
    ], style={"width": "30%", "display": "inline-block"}),

    html.Div([
        html.Label("Select Column to Plot:"),
        dcc.Dropdown(id="column-dropdown"),
    ], style={"width": "30%", "display": "inline-block", "marginLeft": "20px"}),

    dcc.Graph(id="data-graph"),
])

@app.callback(
    Output("column-dropdown", "options"),
    Output("column-dropdown", "value"),
    Input("file-dropdown", "value")
)
def update_column_dropdown(selected_file):
    if selected_file:
        file_data = data_store.get(selected_file)
        if file_data is not None:
            columns = [{"label": col, "value": col} for col in file_data.columns]
            return columns, columns[0]["value"] if columns else None
    return [], None

@app.callback(
    Output("data-graph", "figure"),
    Input("file-dropdown", "value"),
    Input("column-dropdown", "value")
)
def update_graph(selected_file, selected_column):
    if selected_file and selected_column:
        try:
            file_data = data_store.get(selected_file)
            if file_data is not None and selected_column in file_data.columns:
                file_data["Time"] = pd.to_numeric(file_data["Time"], errors='coerce')

                file_data = file_data.dropna(subset=["Time", selected_column])

                print(f"Columns in {selected_file}: {file_data.columns.tolist()}")
                print(f"First few rows of {selected_file}:")
                print(f"Generating graph for {selected_column} vs Time")
                print(file_data.head())  

                # Generate the plot
                fig = px.line(file_data, x="Time", y=selected_column, title=f"{selected_column} vs Time")
                return fig
        except Exception as e:
            print(f"Error in updating graph: {e}")

    return {}

if __name__ == "__main__":
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
        print(f"Data directory '{data_directory}' created. Place your CSV files in this directory.")
    else:
        print(f"Dash is running on http://127.0.0.1:8050/")
    
    app.run_server(debug=True)

