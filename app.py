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
bgColor = '#D3D3D3'

url = 'https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/data/master.csv'
df = pd.read_csv(url)
cols = list(df['Abrv'].unique())

abrvDict = {'AL':'Alaska',
            'AZ':'Arizona',
            'CA':'California',
            'ID':'Idaho',
            'ME':'Maine',
            'MI':'Michigan',
            'MN':'Minnesota',
            'MT':'Montana',
            'NM':'New Mexico',
            'NY':'New York',
            'ND':'North Dakota',
            'TX':'Texas',
            'VT':'Vermont',
            'WA':'Washington'}

########### Figure
def getFig(value, cols, colors):
    figDF = df[df['Abrv']==value]
    data = []
    for i, col in enumerate(cols):
        trace = go.Scatter(
            x = figDF['Year'],
            y = figDF[col],
            mode = 'lines+markers',
            marker = {'color': colors[i]},
            name = col
        )
        data.append(trace)
    layout = go.Layout(
        autosize = True,
        title = f'{abrvDict[value]} Percent Change by Year',
        hovermode = 'closest',
        paper_bgcolor = bgColor,
        plot_bgcolor = bgColor
    )
    fig = go.Figure(data=data,layout=layout)
    return fig

########### Initiate the app
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
    # 'https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/nomargin.css'
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout
app.layout = html.Div(children=[
    html.H1(f'df shape: {df.shape}'),
    html.Div(children=['labor: percent change in labor force (percentage of population able to work)']),
    html.Div(children=['unemp: percent change in unemployment rate (percentage of labor force not working)']),
    html.Div(children=['border: percent change in individuals crossing the border']),
    html.Div(
        dcc.Graph(
            id='popByState',
            figure=getFig('TX', ['labor','unemp','border'],['#67597A','#963D5A','#23CE6B'])
        ),
        style={'width': '69%', 'display': 'inline-block'}#, 'height':'50vh'}
    ),
    html.Div(
    dcc.Dropdown(id='dropdown',
                options=[{'label': i, 'value': i} for i in cols],
                value='TX'
                ),
        style={'width': '29%', 'display': 'inline-block', 'height':'50vh'}
    ),
    html.Div(children=['gdp: percent change in gdp']),
    html.Div(
        dcc.Graph(
            id='gdpByState',
            figure=getFig('TX', ['gdp'],['#586BA4'])
        ),
        style={'width': '69%', 'display': 'inline-block'}#, 'height':'50vh'}
    ),
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ],
    style = {
            'backgroundColor': bgColor,
            }
)

############ Callbacks
@app.callback([Output('gdpByState', 'figure'), Output('popByState', 'figure')],
             [Input('dropdown', 'value')])
def updateFigWith(value):
    toReturn = ''
    if value in cols:
        toReturn = value
    else:
        value = 'TX'
    return getFig(value,['gdp'],['#586BA4']), getFig(value,['labor','unemp','border'],['#67597A','#963D5A','#23CE6B'])

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
