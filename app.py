import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
from tabs import tab1
from tabs import tab2

########### Define a few variables ######

tabtitle = 'Economic EDA 🔍'
sourceurl = 'https://github.com/maxrgnt/pythdc2-project2/blob/master/README.md'
githublink = 'https://github.com/maxrgnt/pythdc2-project2'
bgColor = '#111111'
textColor = '#7f7f7f'

BEA = 'BEA.png'
BLS = 'BLS.png_r=100'
BTS = 'BTS.jpg'

url = 'https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/data/master.csv'
df = pd.read_csv(url)

url2 = 'https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/data/borderCrossing.csv'
choro_df = pd.read_csv(url2)

# Updating column  names to be more 'telling'
df.rename(columns={'gdp':'GDP','labor':'LaborRate','unemp':'UnemploymentRate','border':'Immigration'}, inplace=True)
gdpComp = ['GDP','Immigration']
gdpCompColors = ['#586BA4','#CC5803']
laborComp = ['LaborRate','UnemploymentRate']
laborCompColors = ['#67597A','#963D5A']

cols = list(df['State'].unique())
borders = list(df['US_Border'].unique())

pagetitle = f' Immigration, Unemployment, and GDP by State'
pagesubtitle = f'  [ from {df["Year"].min()} to {df["Year"].max()} ]'

########### Figure
def getFig(value, cols, colors):
    figDF = df[df['State']==value]
    data = []
    for i, col in enumerate(cols):
        trace = go.Scatter(
            x = figDF['Year'],
            y = figDF[col]/100,
            mode = 'lines+markers',
            marker = {'color': colors[i]},
            name = col
        )
        data.append(trace)
    layout = go.Layout(
        #config={'displayModeBar': False},
        template = "plotly_dark",
        autosize = False,
        showlegend = True,
        legend={'x': 0, 'y': 1.1},
        legend_orientation='h',
        xaxis = go.layout.XAxis(
            title = 'Year',
            tickmode = 'linear',
            tick0 = figDF['Year'].min(),
            dtick = 1,
            tickangle = -70
        ),
        yaxis = go.layout.YAxis(
            title = 'Percent Change',
            tickformat = ',.0%'
        ),
        title = f'{list(figDF["State"].unique())[0]} Statistics',
        hovermode = 'closest',
        #margin=go.layout.Margin(l=50, r=50, t=100, b=100, pad= 4),
        #margin=dict(l=20, r=20, t=20, b=20),
        font=dict(
            family="sans-serif",
            size=14,
            color=textColor
        )
    )
    fig = go.Figure(data=data,layout=layout)
    fig.update_yaxes(automargin=True)
    return fig

def getChoro(year):
    thisYear = choro_df[choro_df['Year']==year].groupby('Abrv')[['Value']].sum().reset_index()
    fig = go.Figure(data=go.Choropleth(
        locations=thisYear['Abrv'], # Spatial coordinates
        z = thisYear['Value'].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Purples',
        colorbar_title = 'People',
        )
    )
    fig.update_layout(
        template = "plotly_dark",
        title_text = f'Immigration Data for {year}',
        geo_scope='usa',
        width=1200,
        height=600
    )
    return fig

########### Initiate the app
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle
app.config.suppress_callback_exceptions = True

tabs_styles = {
    'height': '44px'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': f'1px solid {textColor}',
    'borderBottom': f'1px solid {textColor}',
    'backgroundColor': textColor,
    'color': bgColor,
    'padding': '6px'
}

########### Layout
app.layout = html.Div(children=[
    html.Br(),
    html.H2(pagetitle),
    html.H4(pagesubtitle),
    html.Br(),
    html.Div([
        dcc.Tabs(id='tab', value = 'tab1',
            children=[
                dcc.Tab(label = 'Compare Percent Change by State', value = 'tab1', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label = 'Track Immigration Over Time', value = 'tab2', style=tab_style, selected_style=tab_selected_style)
            ],
            colors={
                "border": textColor,
                "primary": bgColor,
                "background": bgColor
            },
            style = tabs_styles
        )
    ]),
    html.Div([
        html.Div(id='tab-content'),
    ], className='twelve columns',
        style={'marginBottom': 50, 'marginTop': 25}),
# Footer Links
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    html.Br(),
# Source Pics
    html.Br(),
    html.Div([
        html.Img(src=app.get_asset_url(BEA), style={'width': '10%', 'height': '10%'}),
        html.Img(src=app.get_asset_url(BLS), style={'width': '10%', 'height': '10%'}),
        html.Img(src=app.get_asset_url(BTS), style={'width': '10%', 'height': '10%'})
    ]),
    html.Br(),
    ],
    style = {
            'backgroundColor': bgColor,
            'color': textColor
            }
)

############ Callbacks
@app.callback(Output('tab-content','children'),
            [Input('tab', 'value')])
def renderTab(tab):
    if tab == 'tab1':
        return tab1.tab_layout
    if tab == 'tab2':
        return tab2.tab_layout

@app.callback([Output('gdpByState', 'figure'), Output('popByState', 'figure')],
             [Input('dropDown', 'value')])
def updateFigWith(value):
    toReturn = ''
    if value in cols:
        toReturn = value
    else:
        value = 'Texas'
    figs = (getFig(value,gdpComp,gdpCompColors),
            getFig(value,laborComp,laborCompColors))
    return figs

@app.callback([Output('dropDown', 'options')],
             [Input('radio', 'value')])
def updateDropDownOptions(value):
    newOptions = list(df[df['US_Border']==value]['State'].unique())
    return [[{'label': i, 'value': i} for i in newOptions]]

@app.callback([Output('dropDown', 'value'), Output('dropDown', 'placeholder')],
             [Input('dropDown', 'options')])
def updateDropDownValue(availableOptions):
    return availableOptions[0]['value'], availableOptions[0]['label']

@app.callback(Output('choropleth', 'figure'),
             [Input('slider', 'value')])
def updateDropDownValue(sliderValue):
    return getChoro(sliderValue)

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
