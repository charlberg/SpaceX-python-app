# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id='entered_site',
        options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
            ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=20000,
        step=1000,
        marks={0: '0', 1000: '1000',
               2000: '2000', 3000: '3000',
               4000: '4000', 5000: '5000',
               6000: '6000', 7000: '7000',
               8000: '8000', 9000: '9000',
               10000: '10000', 11000: '11000',
               12000: '12000', 13000: '13000',
               14000: '14000', 15000: '15000',
               16000: '16000', 17000: '17000',
               18000: '18000', 19000: '19000',
               20000: '20000'
               },
            value=[min_payload, max_payload]
        ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='entered_site', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df,
                     values='class',
                     names='Launch Site',
                     title='Total Successful Launches')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(spacex_df.loc[spacex_df['Launch Site'] == entered_site],
            names='class',
            title='Total Successful Launches for ' + entered_site
        )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='entered_site', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, slider_range):
    low, high = slider_range
    payload_range = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    scatter_df = spacex_df[payload_range]
    if entered_site == 'ALL':
        fig = px.scatter(
            scatter_df,
            x="Payload Mass (kg)",
            y="class",
            title='Payload v. Success: All Sites',
            color="Booster Version Category",
            size='Payload Mass (kg)',
            hover_data=['Booster Version', 'Payload Mass (kg)']
        )
        return fig
    else:
        scatter_df = scatter_df[scatter_df['Launch Site'] == entered_site]
        fig = px.scatter(
            scatter_df,
            x="Payload Mass (kg)",
            y="class",
            title='Payload v. Success for Site ⇉ ' + entered_site,
            color="Booster Version Category",
            size='Payload Mass (kg)',
            hover_data=['Booster Version', 'Payload Mass (kg)']
        )
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
