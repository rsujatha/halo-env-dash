import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

df_corrcon = pd.read_pickle('./data/df_corrcon')
df_corrvar = pd.read_pickle('./data/df_corrvar')
df_corr = pd.read_pickle('./data/df_corr')
df = pd.read_pickle('./data/df_scl')
df0 = pd.read_pickle('./data/df0')


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
tabtitle='beer!'
myheading='Flying Dog Beers'
label1='IBU'
label2='ABV'
githublink='https://github.com/austinlasseter/flying-dog-beers'
sourceurl='https://www.flyingdog.com/beers/'

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
    html.H1(myheading),dcc.Dropdown(id='HaloProperty',placeholder="Select a Halo Property",options=col_options_var,disabled=False),
    dcc.Graph(
        id='flyingdog',
        figure=beer_fig
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A('Data Source', href=sourceurl),
    ]
)

if __name__ == '__main__':
    app.run_server()
