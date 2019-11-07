import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd

########### Define a few variables ######

tabtitle = 'Economic Statistics by State'
sourceurl = 'https://github.com/maxrgnt/pythdc2-project2/blob/master/README.md'
githublink = 'https://github.com/maxrgnt/pythdc2-project2'
bgColor = '#111111'
textColor = '#7f7f7f'

BEA = 'BEA.png'
BLS = 'BLS.png_r=100'
BTS = 'BTS.jpg'

url = 'https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/data/master.csv'
df = pd.read_csv(url)

# Updating column  names to be more 'telling'
df.rename(columns={'gdp':'GDP','labor':'LaborRate','unemp':'UnemploymentRate','border':'Immigration'}, inplace=True)
gdpComp = ['GDP','Immigration']
gdpCompColors = ['#586BA4','#CC5803']
laborComp = ['LaborRate','UnemploymentRate']
laborCompColors = ['#67597A','#963D5A']

cols = list(df['State'].unique())
borders = list(df['US_Border'].unique())

pagetitle = f'Immigration, Unemployment, and GDP by State'
pagesubtitle = f'[ from {df["Year"].min()} to {df["Year"].max()} ]'

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
        template = "plotly_dark",
        autosize = True,
        showlegend = True,
        legend={'x': 0, 'y': 1.2},
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
        title = f'Economic Statistics for {list(figDF["State"].unique())[0]}',
        hovermode = 'closest',
        #margin=go.layout.Margin(l=50, r=50, t=100, b=100, pad= 4),
        font=dict(
            family="sans-serif",
            size=14,
            color=textColor
        )
    )
    fig = go.Figure(data=data,layout=layout)
    return fig

########### Initiate the app
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout
app.layout = html.Div(children=[
    html.Br(),
    html.H2(pagetitle),
    html.H4(pagesubtitle),
# Guide - alt + space to get 'hard' space below
    html.Div([
        dcc.Markdown('''
             * **LaborRate**:                    Δ % of population able to work
             * **UnemploymentRate**:    Δ % of labor force not working
             * **Immigration**:                 Δ inbound border crossing *not necessarily permanent*
             * **GDP**:                              Δ gross domestic product
            ''')
    ]),
    html.Br(),
# Radio Buttons
    html.Div([
        html.Div([
            dcc.RadioItems(
                id = 'radio',
                options=[{'label': i, 'value': i} for i in borders],
                labelStyle={'display': 'inline-block', 'color': textColor},
                inputStyle={"margin-right": "50px"},
                value=borders[0]
            ),
        ],
        style={'width': '24%', 'color': 'lightgray'},
        className = "twelve columns"),
    ], className = "row"),
    html.Br(),
# Drop Down
    html.Div([
        html.Div([
            dcc.Dropdown(id='dropDown',
                options=[{'label': i, 'value': i} for i in cols]
            ),
        ],
        style={'width': '24%', 'color': bgColor},
        className = "twelve columns"),
    ], className = "row"),
    html.Br(),
# Graphs
    html.Div([
        html.Div(
            dcc.Graph(
                id='popByState',
            ),
            style={'width': '47%'},
            className = "six columns"
        ),
        html.Div(
            dcc.Graph(
                id='gdpByState',
            ),
            style={'width': '47%'},#, 'height': 150},
            className = "six columns"),
    ], className = "row"),
    html.Br(),
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

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
