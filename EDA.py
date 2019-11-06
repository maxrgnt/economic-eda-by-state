
# coding: utf-8

# <a href="https://colab.research.google.com/github/maxrgnt/pythdc2-project2/blob/master/EDA.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# In[1]:


# Panel Data
import pandas as pd
# System folders
import os
from pathlib import Path
# Visualization
import plotly.graph_objs as go
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Read in data

# #### Unemployment

# In[2]:


url = 'https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/data/unemployment.csv'
bls = pd.read_csv(url)
print(bls.shape)
bls.sample(1)


# #### GDP

# In[7]:


url = 'https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/data/pctChangeGDP.csv'
bea = pd.read_csv(url)
print(bea.shape)
bea.sample(1)


# #### Border Crossing

# In[8]:


# read in the data
url='https://raw.githubusercontent.com/maxrgnt/pythdc2-project2/master/data/borderCrossing.csv'
bts = pd.read_csv(url)
print(bts.shape)
bts.sample(1)


# ## User defined functions

# In[21]:


def checkPctChange(df):
  print(df[(df['Abrv']=='TX') & (df['Year']==df['Year'].max()-1)])
  print(df[(df['Abrv']=='TX') & (df['Year']==df['Year'].max())])


# In[22]:


def calcPctChange(df, col, pctChange_id):
    # For year in list of unique years
    for y in list(df['Year'].unique()):
        # States = list of unique states
        states = list(df['Abrv'].unique())
        # For state in list of unique states
        for s in states:
            # If the year (first for loop) is greater than the min, calculate PCT CHANGE
            if y != df['Year'].min():
                # t0 = previous year value
                t0 = df.loc[(df['Year'] == y-1) & (df['Abrv'] == s), col].tolist()[0]
                # t1 = current year value
                t1 = df.loc[(df['Year'] == y) & (df['Abrv'] == s), col].tolist()[0]
                # update dataframe with calculated pctChange as pctChange_id
                df.loc[(df['Year']==y) & (df['Abrv']==s), pctChange_id] = ((t1/t0)-1)*100
            else:
                # update dataframe with 'N/A' because pctChange could not be calculated
                df.loc[(df['Year']==y) & (df['Abrv']==s), pctChange_id] = 'N/A'
    # set drop index for first year where pctChange not calculated
    dropIndex = df.loc[df[pctChange_id]=='N/A'].index
    # drop rows where pctChange = 'N/A'
    df.drop(dropIndex, inplace=True)


# ## Feature Engineering (Calculating Percent Change)

# In[11]:


bts2 = bts.groupby(['Year','Abrv','State','Border'])[['Value']].sum().reset_index()
bts2.sample(1)


# #### Border Pct Change

# In[23]:


bts2.rename(columns={'Border':'US_Border'}, inplace = True)
calcPctChange(bts2, 'Value', 'border')
checkPctChange(bts2)


# #### GDP Pct Change

# In[13]:


bea.rename(columns={'Value':'gdp'}, inplace = True)
checkPctChange(bea)


# #### Unemployment Pct Change

# In[14]:


calcPctChange(bls, 'UnemploymentRate', 'unemp')
calcPctChange(bls, 'LaborRate', 'labor')
checkPctChange(bls)


# ## Merging Dataframes

# In[15]:


bls_cols = ['Year','Abrv','State','unemp','labor']
bea_cols = ['Year','Abrv','State','gdp']
bts2_cols = ['Year','Abrv','State','US_Border','border']
merge_cols = ['Year','State','Abrv']
df = bls[bls_cols].merge(bea[bea_cols], how = 'left', left_on= merge_cols, right_on= merge_cols,sort=True)
df = df.merge(bts2[bts2_cols], how = 'left', left_on=merge_cols, right_on=merge_cols,sort=True)


# In[16]:


# Set columns as ints/floats where needed

df['Year'] = df['Year'].astype(int)
for col in ['border','gdp','unemp','labor']:
  df[col] = df[col].astype(float)


# In[17]:


# "Melt" or "Unpivot" the different PctChange column types into one PctChange and one Value column
df_melt = df.melt(['Year','Abrv','State','US_Border'], var_name='PctChange', value_name='Values')


# In[18]:


df_melt.sample(5)


# ## Export as New CSV

# In[36]:


# save new data structure
# df.to_csv(Path.joinpath(Path.cwd(),'data','master.csv'), index = False)


# ## Play around with Visualizations

# In[ ]:


# sns.set(rc={'figure.figsize':(18,6)})
# sns.lineplot(x = 'Year', y = 'vals', hue = 'cols', ci=None, data = df_melt);
# sns.pairplot(df, vars=['border_pctChange','gdp_pctChange','unemp_pctChange'], kind='reg');


# In[ ]:


# mapbox_access_token = open("assets/mytoken.mapbox_token").read()

# fig = go.Figure(go.Scattermapbox(
#     lat=df['Latitude'],
#     lon=df['Longitude'],
#     mode='markers',
#     marker=go.scattermapbox.Marker(
#         size=20,
#         colorscale='Purples',
#         color=df['Value']
#     ),
#     text=df['Value']

# ))
# fig.update_layout(
#     autosize=True,
#     hovermode='closest',
#     mapbox=go.layout.Mapbox(
#         accesstoken=mapbox_access_token,
#         bearing=0,
#         center=go.layout.mapbox.Center(
#             lat=39.8283,
#             lon=-98.5795
#         ),
#         pitch=0,
#         zoom=3
#     ),
# )
# fig


# In[ ]:


# fig = go.Figure(data=go.Choropleth(
#     locations=df2['StateAbrv'], # Spatial coordinates
#     z = df2['Value'].astype(float), # Data to be color-coded
#     locationmode = 'USA-states', # set of locations match entries in `locations`
#     colorscale = 'Purples',
#     colorbar_title = "Pedestrians",
# ))

# fig.update_layout(
#     title_text = 'Migration',
#     geo_scope='usa', # limite map scope to USA
# )

# fig.show()

