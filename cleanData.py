
# coding: utf-8

# <a href="https://colab.research.google.com/github/maxrgnt/pythdc2-project2/blob/master/Clean2.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# In[1]:


# Panel Data
import pandas as pd
# System folders
import os
from pathlib import Path


# In[2]:


def abbreviate(stateName):
    abrvDict = {'Alaska':'AL',
                'Arizona':'AZ',
                'California':'CA',
                'Idaho':'ID',
                'Maine':'ME',
                'Michigan':'MI',
                'Minnesota':'MN',
                'Montana':'MT',
                'New Mexico':'NM',
                'New York':'NY',
                'North Dakota':'ND',
                'Texas':'TX',
                'Vermont':'VT',
                'Washington':'WA'}
    abrv = ''
    if stateName in abrvDict:
        abrv = abrvDict[stateName]
    return abrv

def safeDrop(df, cols):
    print(df.shape)
    for col in df.columns:
        if col in cols:
            print(f'removing: {col}')
            df.drop([col], axis=1, inplace=True)
    print(df.shape)
    return df


# ## Border Data

# In[66]:


dataPath = Path.joinpath(Path.cwd(),'sourceData','borderCrossing.csv')
df = pd.read_csv(dataPath)
df.sample(3)


# In[67]:


df['Measure'].value_counts()


# In[68]:


# Only interested in Passenger / Pedestrian crossings
people = df['Measure'].str.contains('Passengers|Pedestrians', case = False)


# In[69]:


# Check to see how much data frame shrinks after filtering down
print(f'All measures: {df.shape}')
#df = df[people] # This gave index error when re-running, changed to df.loc
df = df.loc[people]
print(f'Just people: {df.shape}')


# In[70]:


# Break out Location into latitude and longitude,
                # substring from 'POINT( ' to ')' and split on ' ' grabbing first then second element set as float,
if 'Location' in df.columns:
    df['Latitude'] = df['Location'].str[len('POINT ('):-1].str.split(' ').str[1].astype(float)
    df['Longitude'] = df['Location'].str[len('POINT ('):-1].str.split(' ').str[0].astype(float)


# In[71]:


# Drop unnecessary columns
df = safeDrop(df, ['Port Code','Port Name','Location','Unnamed: 0','index'])


# In[72]:


# Get state abrv
df['Abrv'] = df['State'].apply(abbreviate)


# In[73]:


# Handle the Date column
if 'Date' in df.columns:
    df['newDate'] = pd.to_datetime(df['Date'])
    df['Year'] = df['newDate'].dt.year.astype(int)


# In[74]:


# drop unneeded rows
# index of all rows where df['Year'] < 1996
print(df.shape)
dropIndex = df.loc[df['Year'].astype(int)>2018].index
df.drop(dropIndex, inplace=True)
print(df.shape)


# In[75]:


# reorganize columns
df = df[['Abrv','State','Longitude','Latitude','Border','Year','Measure','Value']]


# In[76]:


df.sample(5)


# In[51]:


# Remove non-pedestrian values to shrink file
# df.to_csv(Path.joinpath(Path.cwd(),'data','borderCrossing.csv'), index = False)


# ## GDP Data

# In[10]:


dataPath = Path.joinpath(Path.cwd(),'sourceData','pctChangeGDP.csv')
df = pd.read_csv(dataPath)
df.sample(3)


# In[11]:


# rename GeoName to State
df.rename(columns={'GeoName':'State'}, inplace=True)


# In[12]:


# Get state abrv
df['Abrv'] = df['State'].apply(abbreviate)


# In[15]:


# drop unneeded rows\n",
# index of all rows where df['Abrv'] == ''
print(df.shape)
dropIndex = df.loc[df['Abrv']==''].index
df.drop(dropIndex, inplace=True)
print(df.shape)


# In[16]:


# SAFE DROP
df = safeDrop(df, ['GeoFips'])


# In[17]:


if 'Year' not in df.columns:
  df = pd.melt(df, id_vars=['State','Abrv'], var_name='Year', value_name = 'Value')


# In[21]:


# drop unneeded rows
# index of all rows where df['Year'] < 1996
print(df.shape)
dropIndex = df.loc[df['Year'].astype(int)<1997].index
df.drop(dropIndex, inplace=True)
print(df.shape)


# In[31]:


df.sample(5)


# In[13]:


# Un-pivoting
# df.to_csv(Path.joinpath(Path.cwd(),'data','pctChangeGDP.csv'), index = False)


# ## Unemployment Data

# In[35]:


dataPath = Path.joinpath(Path.cwd(),'sourceData','unemployment.csv')
df = pd.read_csv(dataPath)
df.sample(3)


# In[36]:


# rename GeoName to State
df.rename(columns={'Stata':'State'}, inplace=True)


# In[37]:


# get abbreviations
df['Abrv'] = df['State'].apply(abbreviate)
# drop unneeded rows
# index of all rows where df['Abrv'] == ''
print(df.shape)
dropIndex = df.loc[df['Abrv']==''].index
df.drop(dropIndex, inplace=True)
print(df.shape)


# In[38]:


# drop unneeded rows
# index of all rows where df['Year'] < 1996
print(df.shape)
dropIndex = df.loc[df['Year']<1996].index
df.drop(dropIndex, inplace=True)
print(df.shape)


# In[39]:


for col in ['Unemployed','Employed','LaborForce','Population']:
    if col in list(df.columns):
        df['UnemploymentRate'] = df['Unemployed'].div(df['Employed'])
        df['LaborRate'] = df['LaborForce'].div(df['Population'])


# In[40]:


# drop unneeded columns
df = safeDrop(df, ['FIPS','PercentOfPopulation','PercentOfLaborEmp','PercentOfLaborUnemp','Population','LaborForce','Employed','Unemployed'])


# In[41]:


df.sample(3)


# In[36]:


# Un-pivoting
# df.to_csv(Path.joinpath(Path.cwd(),'data','unemployment.csv'), index = False)

