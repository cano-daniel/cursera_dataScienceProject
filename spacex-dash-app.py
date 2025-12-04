# Import required libraries

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
print(spacex_df.columns)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Launch Site Dashboard", style={'textAlign': 'center'}),
    
    # Dropdown for pie chart
    html.Div([
        html.Label("Select Launch Site for Pie Chart:"),
        dcc.Dropdown(
            id='site-dropdown',
            options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                    [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
            value='ALL',
            placeholder="Select a Launch Site"
        )
    ], style={'width': '50%', 'padding': '20px'}),
    
    # Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    
    # Slider for scatter plot
    html.Div([
        html.Label("Select Payload Mass Range (kg):"),
        dcc.RangeSlider(
            id='payload-slider',
            min=min_payload,
            max=max_payload,
            step=100,
            marks={i: str(i) for i in range(int(min_payload), 
                                           int(max_payload)+1, 500)},
            value=[min_payload, max_payload]
        )
    ], style={'padding': '20px'}),
    
    # Scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# Callback for pie chart (controlled by dropdown)
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Show success rate for all sites
        fig = px.pie(spacex_df, names='Launch Site', 
                     title='Total Success Rate by Launch Site')
    else:
        # Show success/failure for selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Success Rate Distribution for {selected_site}')
    
    return fig

# Callback for scatter plot (controlled by slider)
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('payload-slider', 'value')]
)
def update_scatter_chart(payload_range):
    # Filter data based on payload slider
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                     (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    # Create scatter plot
    fig = px.scatter(filtered_df, 
                     x='Payload Mass (kg)', 
                     y='class',
                     color='Launch Site',
                     title='Payload Mass vs Success Rate',
                     labels={'Payload Mass (kg)': 'Payload Mass (kg)', 
                            'class': 'Success'})
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
