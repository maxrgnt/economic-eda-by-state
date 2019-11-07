import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

url = 'https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/data/master.csv'
df = pd.read_csv(url)
bgColor = '#111111'
textColor = '#7f7f7f'

# Updating column  names to be more 'telling'
df.rename(columns={'gdp':'GDP','labor':'LaborRate','unemp':'UnemploymentRate','border':'Immigration'}, inplace=True)
gdpComp = ['GDP','Immigration']
gdpCompColors = ['#586BA4','#CC5803']
laborComp = ['LaborRate','UnemploymentRate']
laborCompColors = ['#67597A','#963D5A']

cols = list(df['State'].unique())
borders = list(df['US_Border'].unique())

tab_layout = html.Div([
    html.Div([
        html.Br(),
        # Radio Buttons / Drop Down
        html.Div([
            html.Div([
                dcc.RadioItems(
                    id = 'radio',
                    options=[{'label': i, 'value': i} for i in borders],
                    labelStyle={'color': textColor},
                    inputStyle={"margin-right": "30px"},
                    value=borders[0]
                ),
            ],
            style={'width': '20%', 'color': textColor},
            className = "nine columns"),
            html.Div([
                dcc.Dropdown(id='dropDown',
                    options=[{'label': i, 'value': i} for i in cols]
                ),
            ],
            style={'width': '24%', 'color': bgColor},
            className = "nine columns"),
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
        # Guide - alt + space to get 'hard' space below
        html.Div([
            dcc.Markdown('''
                *  **LaborRate**:                     Δ % of population able to work
                *  **UnemploymentRate**:     Δ % of labor force not working
                *  **Immigration**:                  Δ inbound border crossing (*not necessarily permanent*)
                *  **GDP**:                               Δ gross domestic product
                ''')
        ]),
        html.Br(),
    ], className='twelve columns'),
], className='twelve columns')
