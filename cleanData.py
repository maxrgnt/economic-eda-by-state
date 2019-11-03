
# coding: utf-8

# <a href="https://colab.research.google.com/github/maxrgnt/pythdc2-project2/blob/master/Clean2.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# In[2]:


# Panel Data
import pandas as pd
# System folders
import os
from pathlib import Path


# In[1]:


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

# In[37]:


dataPath = Path.joinpath(Path.cwd(),'data','borderCrossing.csv')
df = pd.read_csv(dataPath)
df.sample(3)


# In[38]:


df['Measure'].value_counts()


# In[39]:


# Only interested in Passenger / Pedestrian crossings
people = df['Measure'].str.contains('Passengers|Pedestrians', case = False)


# In[40]:


# Check to see how much data frame shrinks after filtering down
print(f'All measures: {df.shape}')
#df = df[people] # This gave index error when re-running, changed to df.loc
df = df.loc[people]
print(f'Just people: {df.shape}')


# In[41]:


# Break out Location into latitude and longitude,
                # substring from 'POINT( ' to ')' and split on ' ' grabbing first then second element set as float,
if 'Location' in df.columns:
    df['Latitude'] = df['Location'].str[len('POINT ('):-1].str.split(' ').str[1].astype(float)
    df['Longitude'] = df['Location'].str[len('POINT ('):-1].str.split(' ').str[0].astype(float)


# In[42]:


# drop unneeded rows
# index of all rows where df['Year'] < 1996
print(df.shape)
dropIndex = df.loc[df['Year']>2018].index
df.drop(dropIndex, inplace=True)
print(df.shape)


# In[43]:


# Drop unnecessary columns
df = safeDrop(df, ['Port Code','Port Name','Location','Unnamed: 0','index'])


# In[44]:


# Get state abrv
df['Abrv'] = df['State'].apply(abbreviate)


# In[47]:


# Handle the Date column
if 'Date' in df.columns:
    df['newDate'] = pd.to_datetime(df['Date'])
    df['Year'] = df['newDate'].dt.year.astype(int)


# In[48]:


# reorganize columns
df = df[['Abrv','State','Longitude','Latitude','Border','Year','Measure','Value']]


# In[50]:


df.sample(5)


# In[51]:


# Remove non-pedestrian values to shrink file
df.to_csv(Path.joinpath(Path.cwd(),'data','borderCrossing.csv'), index = False)


# ## GDP Data

# In[18]:


dataPath = Path.joinpath(Path.cwd(),'data','pctChangeGDP.csv')
df = pd.read_csv(dataPath)
df.sample(3)


# In[19]:


# rename GeoName to State
df.rename(columns={'GeoName':'State'}, inplace=True)


# In[20]:


# Get state abrv
df['Abrv'] = df['State'].apply(abbreviate)


# In[21]:


# drop unneeded rows\n",
# index of all rows where df['Abrv'] == ''
print(df.shape)
dropIndex = df.loc[df['Abrv']==''].index
df.drop(dropIndex, inplace=True)
print(df.shape)


# In[22]:


# drop unneeded rows
# index of all rows where df['Year'] < 1996
print(df.shape)
dropIndex = df.loc[df['Year']<1996].index
df.drop(dropIndex, inplace=True)
print(df.shape)


# In[23]:


# SAFE DROP
df = safeDrop(df, ['GeoFips'])


# In[24]:


if 'Year' not in df.columns:
  df = pd.melt(df, id_vars=['State','Abrv'], var_name='Year', value_name = 'Value')


# In[27]:


df.sample(5)


# In[28]:


# Un-pivoting
df.to_csv(Path.joinpath(Path.cwd(),'data','pctChangeGDP.csv'), index = False)


# ## Unemployment Data

# In[29]:


dataPath = Path.joinpath(Path.cwd(),'data','unemployment.csv')
df = pd.read_csv(dataPath)
df.sample(3)


# In[30]:


# rename GeoName to State
df.rename(columns={'Stata':'State'}, inplace=True)


# In[31]:


# get abbreviations
df['Abrv'] = df['State'].apply(abbreviate)
# drop unneeded rows
# index of all rows where df['Abrv'] == ''
print(df.shape)
dropIndex = df.loc[df['Abrv']==''].index
df.drop(dropIndex, inplace=True)
print(df.shape)


# In[32]:


# drop unneeded rows
# index of all rows where df['Year'] < 1996
print(df.shape)
dropIndex = df.loc[df['Year']<1996].index
df.drop(dropIndex, inplace=True)
print(df.shape)


# In[33]:


for col in ['Unemployed','Employed','LaborForce','Population']:
    if col in list(df.columns):
        df['UnemploymentRate'] = df['Unemployed'].div(df['Employed'])
        df['LaborRate'] = df['LaborForce'].div(df['Population'])


# In[34]:


# drop unneeded columns
df = safeDrop(df, ['FIPS','PercentOfPopulation','PercentOfLaborEmp','PercentOfLaborUnemp','Population','LaborForce','Employed','Unemployed'])


# In[35]:


df.sample(3)


# In[36]:


# Un-pivoting
df.to_csv(Path.joinpath(Path.cwd(),'data','unemployment.csv'), index = False)

