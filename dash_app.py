import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import gdown

# Load the data
file_id = "1LKSjPVavi-3aujfkxqxIRb0akhoGTEcZ"
url = f"https://drive.google.com/uc?export=download&id={file_id}"
output_path = 'Extracted_SSESystemLog.csv'

gdown.download(url, output_path, quiet=False)

filtered_data = pd.read_csv(output_path)

# Bar Chart Data
camera_counts = filtered_data['view_id'].value_counts().reset_index()
camera_counts.columns = ['view_id', 'frequency']
camera_counts = camera_counts.sort_values(by=['view_id'])
bar_fig = px.bar(
    camera_counts,
    x='view_id',
    y='frequency',
    title="Frequency of 'Video Frame Missing' by Camera",
    labels={'view_id': 'Camera ID', 'frequency': 'Frequency'},
    text='frequency',
    color='frequency'
)
bar_fig.update_layout(template='plotly_white', title_x=0.5, xaxis_type='category', width=500, height=600,
                      title_font=dict(size=15), margin=dict(l=50, r=50, t=50, b=50), )

# Line Graph Data
line_data = filtered_data
line_data['datetime'] = pd.to_datetime(line_data['datetime'])
line_data['date'] = line_data['datetime'].dt.date
line_data = line_data.groupby(['date', 'view_id']).size().reset_index(name='frequency')
line_fig = px.line(
    line_data,
    x='date',
    y='frequency',
    color='view_id',
    title="Daily Frequency of 'Video Frame Missing' by Camera",
    labels={'date': 'Date', 'frequency': 'Frequency', 'view_id': 'Camera ID'},
    markers=True
)
line_fig.update_layout(template='plotly_white', title_x=0.5, width=900, height=300, title_font=dict(size=15),
                       margin=dict(l=50, r=50, t=50, b=50), )

# Heatmap Data
hourly_error_counts = filtered_data
hourly_error_counts['date_hour'] = hourly_error_counts['datetime'].dt.floor('H')
hourly_error_counts = hourly_error_counts.groupby(['date_hour', 'view_id']).size().reset_index(name='frequency')
hourly_error_counts['hour'] = hourly_error_counts['date_hour'].dt.time
hourly_error_counts = hourly_error_counts.sort_values(by=['view_id', 'hour'])
heatmap_fig = px.density_heatmap(
    hourly_error_counts,
    x='hour',
    y='view_id',
    z='frequency',
    title="Heatmap of Hourly Frequency of 'Video Frame Missing' by Camera",
    labels={'hour': 'Hour of Day', 'view_id': 'Camera ID', 'frequency': 'Frequency'},
    color_continuous_scale='turbo'
)
heatmap_fig.update_layout(template='plotly_white', yaxis_type='category', title_x=0.5, width=900, height=300,
                          title_font=dict(size=15), margin=dict(l=50, r=50, t=50, b=50))

# Dash App Setup
app = dash.Dash(__name__)
app.title = "CCTV Error Analysis Dashboard"
server = app.server

app.layout = html.Div(
    [
        html.H1("CCTV Error Analysis Dashboard", style={'textAlign': 'center'}),

        # Layout with two columns
        html.Div(
            [
                # Left Column (Bar Chart)
                html.Div(
                    [
                        dcc.Graph(id='bar-chart', figure=bar_fig)
                    ],
                    style={
                        'width': '35%',  # 48% of the total width
                        'marginRight': '10px',  # Add space between columns
                        'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',  # Optional: Add shadow
                        'padding': '10px',
                        'backgroundColor': 'white',
                        'borderRadius': '8px'
                    }
                ),

                # Right Column (Line Chart and Heatmap stacked)
                html.Div(
                    [
                        # Line Chart
                        html.Div(
                            [
                                dcc.Graph(id='line-chart', figure=line_fig)
                            ],
                            style={
                                'marginBottom': '10px',  # Space between the two charts
                                'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',  # Optional: Add shadow
                                'padding': '5px',
                                'backgroundColor': 'white',
                                'borderRadius': '8px'
                            }
                        ),

                        # Heatmap
                        html.Div(
                            [
                                dcc.Graph(id='heatmap', figure=heatmap_fig)
                            ],
                            style={
                                'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',  # Optional: Add shadow
                                'padding': '5px',
                                'backgroundColor': 'white',
                                'borderRadius': '8px'
                            }
                        )
                    ],
                    style={'width': '65%'}
                )
            ],
            style={
                'display': 'flex',  # Flexbox layout
                'flexDirection': 'row',  # Arrange side by side
                'justifyContent': 'center',  # Center the entire layout
                'alignItems': 'flex-start',  # Align items to the top
                'gap': '5px'  # Space between columns
            }
        )
    ],
    style={
        'backgroundColor': '#f9f9f9',  # Optional: Light background color
        'padding': '5px'  # Padding around the content
    }
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
