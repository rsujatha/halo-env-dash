import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input,Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

colr = ["red","blue", "#17BECF","teal"]
colrr = ["red", "red","blue","blue", "#17BECF","#17BECF","teal","teal"]
lnstyle = ["solid","dot","solid","dot","solid","dot","solid","dot"]
env = ['delta0000-','delta0000-','alpha0001-','alpha0001-','alpha0p30-','alpha0p30-','alpha0p55-','alpha0p55-']
scales=['2r','3r','4r','5r','6r','7r','8r','9r','10r']
scaleconst = np.array([0.5,1.25,1.5,2.5,5,10])

    
col_options = [dict(label=x,value=x) for x in df['MassRange'].unique()]
col_options_var =  [dict(label=x,value=x) for x in df['HaloProperty'].unique()]


########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='darkred'
color2='orange'
mytitle='Beer Comparison'
tabtitle='Halo Environment at Different Scales'
myheading='Fixing Halo Environment, Shuffling Halo Properties Exercise'
label1='IBU'
label2='ABV'
githublink='https://github.com/rsujatha/halo-env-dash'

########### Set up the chart
bitterness = go.Bar(
    x=beers,
    y=ibu_values,
    name=label1,
    marker={'color':color1}
)
alcohol = go.Bar(
    x=beers,
    y=abv_values,
    name=label2,
    marker={'color':color2}
)

beer_data = [bitterness, alcohol]
beer_layout = go.Layout(
    barmode='group',
    title = mytitle
)

beer_fig = go.Figure(data=beer_data, layout=beer_layout)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='flyingdog',
        figure=beer_fig
    ),
    html.A('Code and Data on Github', href=githublink),
    dcc.Dropdown(id='HaloProperty',placeholder="Select a Halo Property",options=col_options_var,disabled=False),dcc.Dropdown(id='MassRange',placeholder="Select a Mass Range",options=col_options),dcc.Checklist(
        id='chkmrk',options=[
            {'label': 'All Combined', 'value': 'combined'},],
        value=['combined']
    ),dcc.Graph(id='graph',figure={}),dcc.Graph(id="graph2",figure={})
    ]
)

if __name__ == '__main__':
    app.run_server()
