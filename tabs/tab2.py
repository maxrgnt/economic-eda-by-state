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

cols = list(df['State'].unique())

tab_layout = html.Div([
    html.Div([
        html.Br(),
        html.Div([
            dcc.Slider(
                id='slider',
                min=1998, max=2018,
                step=1, value=1998,
                marks={ 1998 : {'label': '1998', 'style': {'color': textColor}},
                        2003 : {'label': '2003', 'style': {'color': textColor}},
                        2008 : {'label': '2008', 'style': {'color': textColor}},
                        2013 : {'label': '2013', 'style': {'color': textColor}},
                        2018 : {'label': '2018', 'style': {'color': textColor}}}
            )
        ]),
        html.Br(),
        html.Br(),
        dcc.Graph(
            id='choropleth',
        ),
        html.Br(),
    ], className='nine columns'),
], className='nine columns')
