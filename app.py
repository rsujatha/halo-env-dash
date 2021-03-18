import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Input,Output
import plotly.express as px
import plotly.graph_objects as go


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
tabtitle='interactive application'
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
app = dash.Dash(__name__)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),dcc.Dropdown(id='HaloProperty',placeholder="Select a Halo Property",options=col_options_var,disabled=False),dcc.Dropdown(id='MassRange',placeholder="Select a Mass Range",options=col_options),dcc.Checklist(
        id='chkmrk',options=[
            {'label': 'All Combined', 'value': 'combined'},],
        value=['combined']
    ),dcc.Graph(id='graph',figure={}),dcc.Graph(id="graph2",figure={}),
    html.A('Code and Data on Github', href=githublink),
    ]
)
@app.callback(Output('graph', 'figure'), [Input('MassRange', 'value'),Input('HaloProperty','value'),Input('chkmrk','value')])
def cb(massrange,haloproperty,chkmrkvalue):
    if chkmrkvalue==['combined']:
        fig = px.line(df0,x="Scale",y="Chisquare",color='Environment',facet_col='scaletype',line_dash='scaletype' ,color_discrete_sequence=colr,log_y=True,custom_data=[df0.index]).update_layout(clickmode='event+select')
    else:
        if (massrange==None)or(haloproperty==None):
            fig = go.Figure().update_layout(clickmode='event+select')
        else:
            df_cond = df.query("MassRange==@massrange&HaloProperty==@haloproperty")
            fig = px.line(df_cond,x="Scale",y="Chisquare",color='Environment',facet_col='scaletype',line_dash='scaletype' ,color_discrete_sequence=colr,log_y=True,custom_data=[df_cond.index]).update_layout(clickmode='event+select')
    return fig
@app.callback(Output('graph2','figure'),[Input('MassRange','value'),Input('HaloProperty','value'),Input('graph','clickData'),Input('chkmrk','value')])
def display_selected_data(massrange,haloproperty,clickData,chkmrkvalue):
    if chkmrkvalue==["combined"]:
        fig = go.Figure()      
        if clickData:
            curveno = [point["curveNumber"] for point in clickData["points"]]
            scaleno = [point["x"] for point in clickData["points"]]
            envmnt = env[int(curveno[0])]
            if np.mod(int(curveno[0]),2)==0:
                df_corrcond = df_corrvar.query("Environment==@envmnt")
            else:
                df_corrcond = df_corrcon.query("Environment==@envmnt")
            fig = px.line(df_corrcond,x="radialdistance",y="xir",color='Quartile',line_group = 'MassRange',facet_col='HaloProperty',animation_frame="Scale",line_dash_sequence=[lnstyle[curveno[0]],lnstyle[curveno[0]]],color_discrete_sequence=[colrr[curveno[0]],colrr[curveno[0]]],log_y=True,log_x=True, range_y=[0.0005, 100])
            fig2 = px.scatter(df_corr,x='radialdistance',y='xir',color='Quartile',symbol='Quartile',facet_col='HaloProperty',symbol_sequence=['5','6'],color_discrete_sequence=['black'])
            if np.mod(int(curveno[0]),2)==0:
                activeslide =scaleno[0]-2
            else:
                activeslide = int(np.argwhere(scaleconst==scaleno[0])[0,0])
            fig.layout['sliders'][0]['active'] = activeslide
            fig = go.Figure(data=fig['frames'][activeslide]['data'], frames=fig['frames'], layout=fig.layout)
            fig.add_traces([fig2.data[0],fig2.data[1],fig2.data[2],fig2.data[3],fig2.data[4],fig2.data[5],fig2.data[6],fig2.data[7],fig2.data[8],fig2.data[9]])
            print (fig2.data[5])
        else:
            fig = go.Figure()
    else:
        if clickData:
            if (massrange==None)or(haloproperty==None):
                fig = go.Figure()
            else:
                df_corrcond = df_corr.query("MassRange==@massrange&HaloProperty==@haloproperty")
                curveno = [point["curveNumber"] for point in clickData["points"]]
                scaleno = [point["x"] for point in clickData["points"]]
                envmnt = env[int(curveno[0])]
                upper = 'upper'
                lower = 'lower'
                up='up'
                low='low'
                if np.mod(int(curveno[0]),2)==0:
                    df_corrcond = df_corrvar.query("MassRange==@massrange&HaloProperty==@haloproperty&Environment==@envmnt")
                else:
                    df_corrcond = df_corrcon.query("MassRange==@massrange&HaloProperty==@haloproperty&Environment==@envmnt")
            
                df_corrcondlow0 = df_corr.query("MassRange==@massrange&HaloProperty==@haloproperty&Quartile==@lower")
                df_corrcondup0 = df_corr.query("MassRange==@massrange&HaloProperty==@haloproperty&Quartile==@upper")
                if massrange=='0.96-4e12':
                    scalar=5
                elif massrange=='1e13-1e14':
                    scalar=1
                elif massrange=='7e13-2e15':
                    scalar=0.2
                df_corrcond.loc[:,"xir"]*=scalar
                df_corrcond.loc[:,"xirerror"]*=scalar
                df_corrcondlow0.loc[:,"xir"]*=scalar
                df_corrcondlow0.loc[:,"xirerror"]*=scalar
                df_corrcondup0.loc[:,"xir"]*=scalar
                df_corrcondup0.loc[:,"xirerror"]*=scalar
                fig= px.line(df_corrcond,x="radialdistance",y="xir",color='Quartile',animation_frame="Scale",line_dash_sequence=[lnstyle[curveno[0]],lnstyle[curveno[0]]],color_discrete_sequence=[colrr[curveno[0]],colrr[curveno[0]]],log_y=True,log_x=True, range_y=[0.001, 40])
                if np.mod(int(curveno[0]),2)==0:
                    activeslide =scaleno[0]-2
                else:
                    activeslide = int(np.argwhere(scaleconst==scaleno[0])[0,0])
                fig.layout['sliders'][0]['active'] = activeslide
                fig = go.Figure(data=fig['frames'][activeslide]['data'], frames=fig['frames'], layout=fig.layout)
                fig.add_traces([go.Scatter(x=df_corrcondup0['radialdistance'], y=df_corrcondup0['xir'],mode='markers',marker_color='#000000',marker = dict(size = 10, symbol = 5),error_y=dict(type='data', array=df_corrcondup0['xirerror'],visible=True)),
                 go.Scatter(x=df_corrcondlow0['radialdistance'], y=df_corrcondlow0['xir'],mode='markers',marker_color='#000000',marker = dict(size = 10, symbol = 6),error_y=dict(type='data', array=df_corrcondlow0['xirerror'],visible=True)),])             
        else:
            fig = go.Figure()
    return fig

@app.callback(Output('HaloProperty','disabled'),Input('chkmrk','value'),)
def update_dropdown(value):
    if value==['combined']:
        return True
    else:
        return False

@app.callback(Output('MassRange','disabled'),Input('chkmrk','value'),)
def update_dropdown(value):
    if value==['combined']:
        return True
    else:
        return False
    

if __name__ == '__main__':
    app.run_server()
