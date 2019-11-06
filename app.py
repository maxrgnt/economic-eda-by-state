import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd

########### Define a few variables ######

tabtitle = 'Border Crossing v. GDP'
sourceurl = 'https://github.com/maxrgnt/pythdc2-project2/blob/master/README.md'
githublink = 'https://github.com/maxrgnt/pythdc2-project2'
bgColor = '#111111'

url = 'https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/data/master.csv'
df = pd.read_csv(url)
cols = list(df['State'].unique())
borders = list(df['US_Border'].unique())

pagetitle = f'Border Crossing v. GDP from {df["Year"].min()} to {df["Year"].max()}'

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
        xaxis = go.layout.XAxis(
           tickmode = 'linear',
           tick0 = figDF['Year'].min(),
           dtick = 1
        ),
        yaxis = go.layout.YAxis(
            tickformat = ',.0%'
        ),
        # title = f'{list(figDF["State"].unique())[0]} Percent Change by Year',
        hovermode = 'closest',
        margin=go.layout.Margin(l=10, r=0, t=0, b=10)
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
    html.H1(pagetitle),
    html.Div([
        dcc.Markdown('''
            * **labor**:  percent change in labor force (percentage of population able to work)
            * **unemp**:  percent change in unemployment rate (percentage of labor force not working)
            * **border**: percent change in individuals crossing the border
            * **gdp**:    percent change in gdp
            ''')
    ]),
    html.Br(),
#
    html.Div([
        html.Div([
            dcc.RadioItems(
                id = 'radio',
                options=[{'label': i, 'value': i} for i in borders],
                labelStyle={'display': 'inline-block'},
                value=borders[0]
            ),
        ],
        style={'width': '24%', 'color': 'lightgray'},
        className = "twelve columns"),
    ], className = "row"),
#
    html.Br(),
#
    html.Div([
        html.Div([
            dcc.Dropdown(id='dropDown',
                options=[{'label': i, 'value': i} for i in cols]
            ),
        ],
        style={'width': '24%', 'color': bgColor},
        className = "twelve columns"),
    ], className = "row"),
#
    html.Br(),
#
    html.Div([
        html.Div(
            dcc.Graph(
                id='popByState',
            ),
            style={'width': '45%'},
            className = "six columns"
        ),
        html.Div(
            dcc.Graph(
                id='gdpByState',
            ),
            style={'width': '45%'},
            className = "six columns"),
    ], className = "row"),
#
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ],
    style = {
            'backgroundColor': bgColor,
            'color': 'lightgray'
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
    figs = (getFig(value,['gdp','border'],['#586BA4','#CC5803']),
            getFig(value,['labor','unemp'],['#67597A','#963D5A']))
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
